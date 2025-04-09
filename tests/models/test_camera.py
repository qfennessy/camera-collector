import pytest
from camera_collector.models.camera import Camera


def test_camera_creation():
    camera = Camera(
        brand="Nikon",
        model="F3",
        year_manufactured=1980,
        type="SLR",
        film_format="35mm",
        condition="excellent"
    )
    assert camera.brand == "Nikon"
    assert camera.model == "F3"
    assert camera.year_manufactured == 1980
    assert camera.type == "SLR"
    assert camera.film_format == "35mm"
    assert camera.condition == "excellent"