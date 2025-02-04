

from GangaCore.testlib.GangaUnitTest import GangaUnitTest


class TestSavannah9008(GangaUnitTest):
    def test_Savannah9008(self):
        from GangaCore.GPI import File, TestApplication

        dv1 = TestApplication()
        dv1.optsfile = File('x')

        dv2 = TestApplication()
        dv2.optsfile = 'x'

        self.assertEqual(dv1.optsfile.name, dv2.optsfile.name)
        self.assertEqual(dv1, dv2)
