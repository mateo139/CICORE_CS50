import pytest
from flask import Flask
from app import app
from utils import (
    geometry_decision,
    get_characteristic_influences,
    z0_calculation,
    hm_and_sigma_vorh_calculation,
    shape_factor_and_allowable_stresses_calculation,
    stresses_verification,
)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_welcome_page(client):
    """Test the welcome page"""
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Welcome" in rv.data


def test_geometry_decision():
    """Test the geometry_decision function"""
    he, be = geometry_decision("p", hp=100, bp=200, dr=10)
    assert he == 80
    assert be == 180


def test_get_characteristic_influences():
    """Test the get_characteristic_influences function"""
    My, N, Fs = get_characteristic_influences("c", My=50, N=100, Fs=30)
    assert My == 50
    assert N == 100
    assert Fs == 30


def test_z0_calculation():
    """Test the z0_calculation function"""
    z0 = z0_calculation(4, 80, -20, 30, 320)
    assert z0 == 96


def test_hm_and_sigma_vorh_calculation():
    """Test the hm_and_sigma_vorh_calculation function"""
    F, hm, sigma_vorh = hm_and_sigma_vorh_calculation(96, 4, 80, -20, 30, 320, 130, 210)
    assert F == 22  # [kN]
    assert hm == 167  # [mm]
    assert sigma_vorh == 16.67  # [N/mm^2]


def test_shape_factor_and_allowable_stresses_calculation():
    """Test the shape_factor_and_allowable_stresses_calculation function"""
    S, sigma_all = shape_factor_and_allowable_stresses_calculation(
        320, 167, 130, 4, 21, te=10
    )
    assert S == 2.9  # [N/mm^2]
    assert sigma_all == 17.54  # [N/mm^2]


def test_2_z0_calculation():
    """Test the z0_calculation function"""
    z0 = z0_calculation(4, 100, -68, 6.2, 230)
    assert z0 == 332


def test_2_hm_and_sigma_vorh_calculation():
    """Test the get_characteristic_influences function"""
    My, N, Fs = get_characteristic_influences("d", My=140, N=280, Fs=30)
    assert My == 100
    assert N == 200
    assert Fs == 30
    """Test the hm_and_sigma_vorh_calculation function"""
    F, hm, sigma_vorh = hm_and_sigma_vorh_calculation(
        332, 4, 100, -68, 6.2, 230, 230, 200
    )
    assert F == 0  # [kN]
    assert hm == 203  # [mm]
    assert sigma_vorh == 10  # [N/mm^2]


def test_2_shape_factor_and_allowable_stresses_calculation():
    """Test the shape_factor_and_allowable_stresses_calculation function"""
    S, sigma_all = shape_factor_and_allowable_stresses_calculation(
        230, 203, 230, 4, 18, te=10
    )
    assert S == 4.2  # [N/mm^2]
    assert sigma_all == 30  # [N/mm^2]


def test_3_shape_factor_and_allowable_stresses_calculation():
    """Test the shape_factor_and_allowable_stresses_calculation function"""
    S, sigma_all = shape_factor_and_allowable_stresses_calculation(
        230, 203, 230, 4, 18, te=20
    )
    assert S == 2.1  # [N/mm^2]
    assert sigma_all == 10.66  # [N/mm^2]


def test_2_z0_calculation():
    """Test the z0_calculation function"""
    z0 = z0_calculation(4, 100, -68, 6.2, 230)
    assert z0 == 332


def test_stresses_verification():
    """Test the stresses_verification function"""
    verification_status = stresses_verification(16.67, 17.54, None)
    assert verification_status == "Fulfilled"
    verification_status = stresses_verification(40, 30, None)
    assert verification_status == "Not fulfilled"
