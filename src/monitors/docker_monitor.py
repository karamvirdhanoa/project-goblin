import logging
from dataclasses import dataclass, field

import docker
from docker.errors import DockerException, NotFound

from src import config

logger = logging.getLogger(__name__)


@dataclass
class ContainerSnapshot:
    name: str
    status: str          # running | exited | restarting | paused | ...
    exit_code: int | None
    restart_count: int
    image: str
    error: str | None = None


@dataclass
class DockerSnapshot:
    containers: list[ContainerSnapshot] = field(default_factory=list)
    error: str | None = None


def collect() -> DockerSnapshot:
    try:
        client = docker.DockerClient(base_url=f"unix://{config.DOCKER_SOCKET_PATH}")
        containers = client.containers.list(all=True)
    except DockerException as exc:
        logger.error("Cannot connect to Docker socket: %s", exc)
        return DockerSnapshot(error=str(exc))

    snapshots = []
    for c in containers:
        try:
            attrs = c.attrs
            state = attrs.get("State", {})
            snapshots.append(ContainerSnapshot(
                name=c.name,
                status=state.get("Status", "unknown"),
                exit_code=state.get("ExitCode"),
                restart_count=attrs.get("RestartCount", 0),
                image=c.image.tags[0] if c.image.tags else c.image.short_id,
            ))
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to read container %s: %s", c.name, exc)
            snapshots.append(ContainerSnapshot(
                name=getattr(c, "name", "unknown"),
                status="unknown",
                exit_code=None,
                restart_count=0,
                image="unknown",
                error=str(exc),
            ))

    logger.debug("Docker snapshot: %d containers", len(snapshots))
    return DockerSnapshot(containers=snapshots)
