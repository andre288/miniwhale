class ContainerNotFoundError(Exception):
    def __init__(self, container_id: str):
        self.container_id = container_id
        super().__init__(f"Container {container_id} not found")
