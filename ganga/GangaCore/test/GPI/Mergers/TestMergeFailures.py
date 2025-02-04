

import os

import pytest
from GangaCore.GPIDev.Base.Proxy import addProxy
from GangaCore.testlib.GangaUnitTest import GangaUnitTest
from GangaCore.testlib.monitoring import run_until_state
from GangaTest.Framework.utils import sleep_until_state

from .CopySplitter import CopySplitter
from .MergerTester import MergerTester

CopySplitter = addProxy(CopySplitter)
MergerTester = addProxy(MergerTester)


class TestMergeFailures(GangaUnitTest):

    def testMergeThatAlwaysFails(self):
        from GangaCore.GPI import Executable, Job, Local, LocalFile

        j = Job()
        j.application = Executable(exe='sh', args=['-c', 'echo foo > out.txt'])
        j.backend = Local()
        j.outputfiles = [LocalFile('out.txt')]
        j.splitter = CopySplitter()
        j.postprocessors = MergerTester(files=['out.txt'])

        j.submit()

        assert run_until_state(j, 'failed', timeout=60)
        assert os.path.exists(os.path.join(j.outputdir, 'out.txt.merge_summary')), 'Summary file should be created'

    def testMergeThatAlwaysFailsIgnoreFailed(self):
        from GangaCore.GPI import Executable, Job, Local, LocalFile

        j = Job()
        j.application = Executable(exe='sh', args=['-c', 'echo foo > out.txt'])
        j.backend = Local()
        j.outputfiles = [LocalFile('out.txt')]
        j.splitter = CopySplitter()
        j.postprocessors = MergerTester(files=['out.txt'], ignorefailed=True)

        j.submit()

        assert run_until_state(j, 'failed', timeout=60)
        assert os.path.exists(os.path.join(j.outputdir, 'out.txt.merge_summary')), 'Summary file should be created'

    def testMergeThatAlwaysFailsOverwrite(self):
        from GangaCore.GPI import Executable, Job, Local, LocalFile

        j = Job()
        j.application = Executable(exe='sh', args=['-c', 'echo foo > out.txt'])
        j.backend = Local()
        j.outputfiles = [LocalFile('out.txt')]
        j.splitter = CopySplitter()
        j.postprocessors = MergerTester(files=['out.txt'], overwrite=True)

        j.submit()

        assert run_until_state(j, 'failed', timeout=60)
        assert os.path.exists(os.path.join(j.outputdir, 'out.txt.merge_summary')), 'Summary file should be created'

    def testMergeThatAlwaysFailsFlagsSet(self):
        from GangaCore.GPI import Executable, Job, Local, LocalFile

        j = Job()
        j.application = Executable(exe='sh', args=['-c', 'echo foo > out.txt'])
        j.backend = Local()
        j.outputfiles = [LocalFile('out.txt')]
        j.splitter = CopySplitter()
        j.postprocessors = MergerTester(
            files=['out.txt'], ignorefailed=True, overwrite=True)

        j.submit()

        assert run_until_state(j, 'failed', timeout=60)
        assert os.path.exists(os.path.join(j.outputdir, 'out.txt.merge_summary')), 'Summary file should be created'

    def testMergeRemoval(self):
        from GangaCore.GPI import Executable, Job, Local, LocalFile, jobs

        # see Savannah 33710
        j = Job()
        jobID = j.id
        # job will run for at least 20 seconds
        j.application = Executable(
            exe='sh', args=['-c', 'sleep 20; echo foo > out.txt'])
        j.backend = Local()
        j.outputfiles = [LocalFile('out.txt')]
        j.splitter = CopySplitter()
        j.postprocessors = MergerTester(files=['out.txt'])

        j.postprocessors[0].ignorefailed = True
        j.postprocessors[0].alwaysfail = True
        j.postprocessors[0].wait = 10

        j.submit()
        run_until_state(j, state='running')
        j.remove()

        with pytest.raises(KeyError):
            jobs(jobID)
