import heapq

from constants import ZoneType
from drone import Drone
from map_config import MapConfig
from text_printer import Printer
from typing import Optional
from exceptions import PathError


class Initiator:
    """Loads a validated map and runs the multi-drone simulation."""

    def __init__(self, config: Optional[MapConfig]) -> None:
        """Greet the user and store the map config to simulate.

        Args:
            config: The parsed map, or ``None`` if loading failed.

        Attributes set here (besides ``config`` and ``printer``):
            drones: The fleet from the last ``run_simulation()`` call,
                each with its final state (empty until then).
            turns: One formatted ``D<id>-<zone>`` line per simulation
                turn, in order (VII.5), from the last run.
            turn_moves: Same data as ``turns``, but as
                ``(drone_id, label)`` pairs per turn instead of a
                pre-joined string, for callers that want to iterate
                without re-parsing the text.
        """
        self.config = config
        self.printer: Printer = Printer()
        self.drones: list[Drone] = []
        self.turns: list[str] = []
        self.turn_moves: list[list[tuple[int, str]]] = []
        self.printer.print_by_letter(
            "Initiating the simulation...",
            0.1,
            0.5,
            "\033[92m"
        )

    def fill_hub_connections(self) -> None:
        """Attach every ``Connection`` to the hubs it links.

        Rebuilds each hub's connection list from scratch, so calling
        this more than once (e.g. once from ``find_path_to_end`` and
        again from ``run_simulation``) stays safe instead of
        duplicating entries.

        Raises:
            PathError: If the config isn't loaded.
        """
        if self.config is None:
            raise PathError("Sonthing was wrong")
        for key, hub in self.config.hubs.items():
            hub.connection = []
            for connection in self.config.connections:
                if connection.pos1 == key:
                    hub.connection.append(connection)
                elif connection.pos2 == key:
                    hub.connection.append(connection)

    def find_path_to_end(self) -> bool:
        """Check whether the end hub is reachable from the start hub.

        An iterative DFS over the hub graph, ignoring movement costs
        and capacities, and refusing to cross ``blocked`` hubs.

        Returns:
            True if at least one valid route exists.

        Raises:
            PathError: If the config isn't loaded.
        """
        if self.config is None:
            raise PathError("The config is not loaded.")
        self.fill_hub_connections()
        self.printer.print_by_letter(
            "Serching a valid way to the end...",
            0.02,
            2,
            "\033[92m"
        )
        start = self.config.gates.entry.name
        end = self.config.gates.exit.name
        visited: set[str] = set()
        to_visit = [start]
        while to_visit:
            current = to_visit.pop()
            if current == end:
                return True
            if current in visited:
                continue
            visited.add(current)
            hub = self.config.hubs.get(current)
            if hub is None:
                continue
            for connection in hub.connection:
                if connection.pos1 == current:
                    neighbor = connection.pos2
                else:
                    neighbor = connection.pos1
                if neighbor in visited:
                    continue
                neighbor_hub = self.config.hubs.get(neighbor)
                if neighbor_hub is not None:
                    if neighbor_hub.zone == "blocked":
                        continue
                to_visit.append(neighbor)
        return False

    @staticmethod
    def _zone_cost(zone: ZoneType) -> Optional[int]:
        """Turns needed to move into a hub of the given zone type.

        Args:
            zone: The destination hub's zone type.

        Returns:
            The movement cost in turns, or ``None`` if the zone is
            ``blocked`` and can never be entered.
        """
        if zone == "blocked":
            return None
        if zone == "restricted":
            return 2
        return 1

    def _shortest_path(self) -> list[str]:
        """Compute the cheapest route from the entry to the exit hub.

        Runs Dijkstra's algorithm over the hub graph, weighting each
        step by the destination hub's zone cost (see ``_zone_cost``)
        and refusing to route through ``blocked`` hubs.

        Returns:
            Hub names from the entry hub to the exit hub, inclusive.

        Raises:
            PathError: If the config isn't loaded, or no route
                avoiding ``blocked`` hubs connects entry to exit.
        """
        if self.config is None:
            raise PathError("The config is not loaded.")
        config = self.config
        start = config.gates.entry.name
        end = config.gates.exit.name

        distances: dict[str, int] = {start: 0}
        previous: dict[str, str] = {}
        visited: set[str] = set()
        queue: list[tuple[int, str]] = [(0, start)]

        while queue:
            dist, current = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)
            if current == end:
                break
            hub = config.hubs.get(current)
            if hub is None:
                continue
            for connection in hub.connection:
                if connection.pos1 == current:
                    neighbor = connection.pos2
                else:
                    neighbor = connection.pos1
                if neighbor in visited:
                    continue
                neighbor_hub = config.hubs.get(neighbor)
                if neighbor_hub is None:
                    continue
                cost = self._zone_cost(neighbor_hub.zone)
                if cost is None:
                    continue
                new_dist = dist + cost
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(queue, (new_dist, neighbor))

        if end not in visited:
            raise PathError("No valid path between start and end.")

        path = [end]
        while path[-1] != start:
            path.append(previous[path[-1]])
        path.reverse()
        return path

    def _connection_capacities(self) -> dict[frozenset[str], int]:
        """Map each connection's endpoints to its crossing capacity.

        Returns:
            A lookup from ``{pos1, pos2}`` to ``max_link_capacity``.

        Raises:
            PathError: If the config isn't loaded.
        """
        if self.config is None:
            raise PathError("The config is not loaded.")
        return {
            frozenset((c.pos1, c.pos2)): c.capacity
            for c in self.config.connections
        }

    def _create_drones(self, path: list[str]) -> list[Drone]:
        """Create the fleet, each following the same shared route.

        Args:
            path: The route (from ``_shortest_path``) every drone
                will follow from entry to exit.

        Returns:
            One ``Drone`` per drone requested by the map, numbered
            from 1.

        Raises:
            PathError: If the config isn't loaded.
        """
        if self.config is None:
            raise PathError("The config is not loaded.")
        drones = []
        for drone_id in range(1, self.config.nb_drones + 1):
            drone = Drone(drone_id, self.config)
            drone.set_path(path)
            drones.append(drone)
        return drones

    def run_simulation(self) -> None:
        """Run the turn-based multi-drone simulation to completion.

        Every drone follows the same cost-optimal shared path.
        Each turn: in-flight drones (crossing a ``restricted`` link)
        advance first; then the remaining drones are offered a move,
        processed from the one closest to the end hub to the one
        closest to the start, so a hub freed by a drone ahead can be
        used the same turn by the drone behind it (VII.3). A drone
        that can't move (zone or connection at capacity) simply
        waits and is left out of that turn's line.

        Stores the outcome in ``self.drones``, ``self.turns`` and
        ``self.turn_moves`` (see ``__init__``) instead of returning
        it, so callers can inspect or loop over it afterwards.

        Raises:
            PathError: If the config isn't loaded, no route exists,
                or a turn goes by with no drone able to move (which
                would indicate a scheduling bug, since a single
                shared path can never truly deadlock).
        """
        if self.config is None:
            raise PathError("The config is not loaded.")
        config = self.config
        self.fill_hub_connections()

        path = self._shortest_path()
        self.drones = self._create_drones(path)
        drones = self.drones
        self.turns = []
        self.turn_moves = []
        start_name = config.gates.entry.name
        end_name = config.gates.exit.name
        connection_capacity = self._connection_capacities()
        connection_usage: dict[frozenset[str], int] = {}
        hub_occupancy: dict[str, int] = {}
        transit_keys: dict[int, frozenset[str]] = {}

        def hub_has_room(name: str) -> bool:
            if name in (start_name, end_name):
                return True
            limit = config.hubs[name].max_drones
            if limit is None:
                return False
            return hub_occupancy.get(name, 0) < limit

        def enter_hub(name: str) -> None:
            if name not in (start_name, end_name):
                hub_occupancy[name] = hub_occupancy.get(name, 0) + 1

        def leave_hub(name: str) -> None:
            if name not in (start_name, end_name):
                hub_occupancy[name] = hub_occupancy.get(name, 0) - 1

        def connection_has_room(key: frozenset[str]) -> bool:
            return connection_usage.get(key, 0) < connection_capacity[key]

        while not all(drone.is_delivered for drone in drones):
            moves: list[tuple[int, str]] = []
            just_arrived: set[int] = set()

            for drone in drones:
                if not drone.is_in_transit:
                    continue
                arrived = drone.advance_transit()
                if arrived:
                    key = transit_keys.pop(drone.id)
                    connection_usage[key] -= 1
                    just_arrived.add(drone.id)
                moves.append((drone.id, drone.current_label))

            order = sorted(
                drones, key=lambda d: (-d.path_progress, d.id)
            )
            one_turn_releases: list[frozenset[str]] = []
            for drone in order:
                if drone.is_delivered or drone.is_in_transit:
                    continue
                if drone.id in just_arrived:
                    continue
                next_hub = drone.next_hub()
                if next_hub is None:
                    continue
                current_hub = drone.current_hub
                key = frozenset((current_hub, next_hub))
                if not hub_has_room(next_hub):
                    continue
                if not connection_has_room(key):
                    continue

                cost = self._zone_cost(config.hubs[next_hub].zone)
                assert cost is not None

                leave_hub(current_hub)
                enter_hub(next_hub)
                connection_usage[key] = connection_usage.get(key, 0) + 1

                if cost == 1:
                    drone.move_to(next_hub)
                    one_turn_releases.append(key)
                else:
                    drone.start_transit(
                        f"{current_hub}-{next_hub}", next_hub, cost - 1
                    )
                    transit_keys[drone.id] = key
                moves.append((drone.id, drone.current_label))

            for key in one_turn_releases:
                connection_usage[key] -= 1

            if not moves:
                raise PathError(
                    "Simulation deadlocked: no drone could move "
                    "this turn."
                )

            moves.sort()
            self.turn_moves.append(moves)
            self.turns.append(
                " ".join(f"D{drone_id}-{label}" for drone_id, label in moves)
            )
