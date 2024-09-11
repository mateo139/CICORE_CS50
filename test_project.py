import unittest
from unittest.mock import patch
from project import main, z0_calculation, hm_and_sigma_vorh_calculation, screws_in_pressured_area_check

class TestIntegration(unittest.TestCase):

    @patch('builtins.input', side_effect=[
        'b',   # wybór podkładki elastomerowej
        '230', '230',  # he, be
        'c',  # dane charakterystyczne
        '6.2', '-68', '100',  # My, N, Fs
        '4', '200', '18'  # n, e2, d
    ])
    def test_case_1(self, mock_input):
        """Test dla przypadku 1 - tylko ściskanie przekroju"""
        # Symulacja pełnej ścieżki danych i wywołań w main()
        he, be = 230, 230
        My, N, Fs = 6.2, -68, 100
        n, e2, d = 4, 200, 18
        
        # Obliczenie z0
        z0 = z0_calculation(n, Fs, N, My, he)
        self.assertAlmostEqual(z0, 332, delta=1)

        # Obliczenie hm i sigma_vorh
        hm, sigma_vorh = hm_and_sigma_vorh_calculation(z0, n, Fs, N, My, he, be, e2)
        self.assertAlmostEqual(hm, 203, delta=1)
        self.assertAlmostEqual(sigma_vorh, -10, delta=1)

        # Obliczenie sigma_zul
        te = 5  # Zakładam, że te jest stałe
        sigma_zul = screws_in_pressured_area_check(he, hm, be, d, n, te)
        self.assertAlmostEqual(sigma_zul, 30, delta=0.1)

    @patch('builtins.input', side_effect=[
        'b',   # wybór podkładki elastomerowej
        '230', '230',  # he, be
        'c',  # dane charakterystyczne
        '60', '10', '10',  # My, N, Fs
        '4', '200', '18'  # n, e2, d
    ])
    def test_case_2(self, mock_input):
        """Test dla przypadku 2 - ściskanie i rozciąganie przekroju"""
        # Symulacja pełnej ścieżki danych i wywołań w main()
        he, be = 230, 230
        My, N, Fs = 60, 10, 10
        n, e2, d = 4, 200, 18

        # Obliczenie z0
        z0 = z0_calculation(n, Fs, N, My, he)
        self.assertAlmostEqual(z0, 2, delta=1)

        # Obliczenie hm i sigma_vorh
        hm, sigma_vorh = hm_and_sigma_vorh_calculation(z0, n, Fs, N, My, he, be, e2)
        self.assertAlmostEqual(hm, 119, delta=1)
        self.assertAlmostEqual(sigma_vorh, -14.75, delta=0.1)

        # Obliczenie sigma_zul
        te = 5  # Zakładam, że te jest stałe
        sigma_zul = screws_in_pressured_area_check(he, hm, be, d, n, te)
        self.assertAlmostEqual(sigma_zul, 30, delta=0.1)

if __name__ == "__main__":
    unittest.main()
