from wyflask.services import Service
from wyflask.repositories import Repository

def test_service_creation():
    class MyService(Service):
        pass
    
    svc = MyService()
    assert isinstance(svc, Service)

def test_repository_creation():
    class MyRepository(Repository):
        pass
    
    repo = MyRepository()
    assert isinstance(repo, Repository)
