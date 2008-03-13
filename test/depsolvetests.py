import unittest
from testbase import *

class DepsolveTests(DepsolveTests):
    def testEmpty(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        self.tsInfo.addInstall(po)
        self.tsInfo.remove(po.pkgtup)
        self.assertEquals('empty', *self.resolveCode())

    def testInstallSinglePackageNoRequires(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        self.tsInfo.addInstall(po)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po,))

    def testInstallSinglePackageRequireNotProvided(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', None, (None, None, None))
        self.tsInfo.addInstall(po)

        self.assertEquals('err', *self.resolveCode())

    def testInstallSinglePackageRequireInstalled(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', None, (None, None, None))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1', '1', None, 'i386')
        self.rpmdb.addPackage(ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, ipo))

    def testInstallSinglePackageRequireInstalledRequireNotProvided(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', None, (None, None, None))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1', '2', None, 'i386')
        po.addRequires('zap', None, (None, None, None))
        self.rpmdb.addPackage(ipo)

        self.assertEquals('err', *self.resolveCode())

    def testInstallSinglePackageRequireInstalledRequireInstall(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', None, (None, None, None))
        self.tsInfo.addInstall(po)
        po2 = FakePackage('zap', '1', '2', None, 'i386')
        self.tsInfo.addInstall(po2)

        ipo = FakePackage('zip', '1', '3', None, 'i386')
        po.addRequires('zap', None, (None, None, None))
        self.rpmdb.addPackage(ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po2, ipo))


    def testInstallSinglePackageRequireVer1NotProvided(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'EQ', (None, '1.3', '2'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.0', '2', None, 'i386')
        self.rpmdb.addPackage(ipo)
        
        self.assertEquals('err', *self.resolveCode())

    def testInstallSinglePackageRequireVer1Installed(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'EQ', (None, '1.3', '2'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '2', None, 'i386')
        self.rpmdb.addPackage(ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, ipo))

    def testInstallSinglePackageRequireVer2NotProvided(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'EQ', (None, '1.3', '4'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '2', None, 'i386')
        self.rpmdb.addPackage(ipo)
        
        self.assertEquals('err', *self.resolveCode())

    def testInstallSinglePackageRequireVer2Installed(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'EQ', (None, '1.3', '4'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '4', None, 'i386')
        self.rpmdb.addPackage(ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, ipo))

    def testInstallSinglePackageRequireVer3NotProvided(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'GE', ('1', '1.3', '4'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '4', '0', 'i386')
        self.rpmdb.addPackage(ipo)
        
        self.assertEquals('err', *self.resolveCode())

    def testInstallSinglePackageRequireVer3Installed(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'GE', ('2', '1.3', '4'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '4', '2', 'i386')
        self.rpmdb.addPackage(ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, ipo))

    def testInstallSinglePackageRequireVer4NotProvided(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'LT', ('2', '1.3', '4'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '4', '2', 'i386')
        self.rpmdb.addPackage(ipo)
        
        self.assertEquals('err', *self.resolveCode())

    def testInstallSinglePackageRequireVer4_1Installed(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'LT', ('2', '1.3', '4'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.0', '4', '2', 'i386')
        self.rpmdb.addPackage(ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, ipo))
    def testInstallSinglePackageRequireVer4_2Installed(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'LT', ('2', '1.3', '4'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '3', '2', 'i386')
        self.rpmdb.addPackage(ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, ipo))
    def testInstallSinglePackageRequireVer4_3Installed(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'LT', ('2', '1.3', '4'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '4', None, 'i386')
        self.rpmdb.addPackage(ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, ipo))
    def testInstallSinglePackageRequireVer4_4Installed(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'LT', ('2', '1.3', '4'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '4', '1', 'i386')
        self.rpmdb.addPackage(ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, ipo))
    def testInstallSinglePackageRequireVer4_5Installed(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'LT', ('2', '1.3', '4'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '0.3', '4', '2', 'i386')
        self.rpmdb.addPackage(ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, ipo))

    def testInstallSinglePackageRequireXtraBadVer(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'EQ', ('2', '1.3', '4'))
        po.addRequires('zap', 'EQ', ('2', '1.3', '4'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '4', '2', 'i386')
        self.rpmdb.addPackage(ipo)

        xpo = FakePackage('zap', '1.3', '4', '0', 'i386')
        self.xsack.addPackage(xpo)

        self.assertEquals('err', *self.resolveCode())

    def testInstallSinglePackageRequireXtra(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'EQ', ('2', '1.3', '4'))
        po.addRequires('zap', 'EQ', ('4', '2.6', '8'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '4', '2', 'i386')
        self.rpmdb.addPackage(ipo)
        
        xpo = FakePackage('zap', '2.6', '8', '4', 'i386')
        self.xsack.addPackage(xpo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, ipo, xpo))
        
    def testInstallSinglePackageRequireInstalledRequireXtra(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'EQ', ('2', '1.3', '4'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '4', '2', 'i386')
        ipo.addRequires('zap', 'EQ', ('4', '2.6', '8'))
        self.rpmdb.addPackage(ipo)
        
        xpo = FakePackage('zap', '2.6', '8', '4', 'i386')
        self.xsack.addPackage(xpo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, ipo))
        
    def testInstallSinglePackageRequireUpgradeRequireXtraErr(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'EQ', ('4', '2.6', '8'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '4', '2', 'i386')
        ipo.addRequires('zap', 'EQ', ('2', '1.3', '3'))
        self.rpmdb.addPackage(ipo)
        
        xpo = FakePackage('zip', '2.6', '8', '4', 'i386')
        xpo.addRequires('zap', 'EQ', ('2', '1.3', '4'))
        self.xsack.addPackage(xpo)
        xpo = FakePackage('zap', '1.3', '4', '2', 'i386')
        xpo.addRequires('zsh', 'EQ', ('2', '4', '8'))
        self.xsack.addPackage(xpo)

        self.assertEquals('err', *self.resolveCode())

    def testInstallSinglePackageRequireUpgradeRequireXtraOk(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'EQ', ('4', '2.6', '8'))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1.3', '4', '2', 'i386')
        ipo.addRequires('zap', 'EQ', ('2', '1.3', '3'))
        self.rpmdb.addPackage(ipo)
        
        xpo = FakePackage('zip', '2.6', '8', '4', 'i386')
        xpo.addRequires('zap', 'EQ', ('2', '1.3', '4'))
        self.xsack.addPackage(xpo)
        xpo2 = FakePackage('zap', '1.3', '4', '2', 'i386')
        self.xsack.addPackage(xpo2)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo, xpo2))
        
    def testInstallSinglePackageRequireMultiXtra(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', 'EQ', ('4', '2.6', '8'))
        self.tsInfo.addInstall(po)

        xpo = FakePackage('zip', '2.6', '8', '4', 'i386')
        xpo.addRequires('zap', 'EQ', ('2', '1.3', '4'))
        self.xsack.addPackage(xpo)
        
        xpo2 = FakePackage('zap', '1.3', '4', '2', 'i386')
        self.xsack.addPackage(xpo2)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo, xpo2))
        
    def testInstallSinglePackageRequireInstalledMultiLib(self):
        po = FakePackage('zsh', '1', '1', None, 'x86_64')
        po.addRequires('zip', None, (None, None, None))
        self.tsInfo.addInstall(po)

        ipo = FakePackage('zip', '1', '3', None, 'i386')
        self.rpmdb.addPackage(ipo)

        xpo = FakePackage('zip', '1', '3', None, 'x86_64')
        self.xsack.addPackage(xpo)
        
        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, ipo))

    def testInstallSinglePackageRequireXtra1MultiLib(self):
        po = FakePackage('zsh', '1', '1', None, 'x86_64')
        po.addRequires('zip', None, (None, None, None))
        self.tsInfo.addInstall(po)

        xpo = FakePackage('zip', '1', '3', None, 'i386')
        self.xsack.addPackage(xpo)
        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo))

    def testInstallSinglePackageRequireXtra2_64MultiLib(self):
        po = FakePackage('zsh', '1', '1', None, 'x86_64')
        po.addRequires('zip', None, (None, None, None))
        self.tsInfo.addInstall(po)

        xpo = FakePackage('zip', '1', '3', None, 'i386')
        self.xsack.addPackage(xpo)
        xpo64 = FakePackage('zip', '1', '3', None, 'x86_64')
        self.xsack.addPackage(xpo64)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo64))

    def testInstallSinglePackageRequireXtra2_32MultiLib(self):
        po = FakePackage('zsh', '1', '1', None, 'i386')
        po.addRequires('zip', None, (None, None, None))
        self.tsInfo.addInstall(po)

        xpo = FakePackage('zip', '1', '3', None, 'i386')
        self.xsack.addPackage(xpo)
        xpo64 = FakePackage('zip', '1', '3', None, 'x86_64')
        self.xsack.addPackage(xpo64)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo))

    def testUpdateSinglePackage(self):
        ipo = FakePackage('zsh', '1', '1', None, 'i386')
        self.rpmdb.addPackage(ipo)

        po = FakePackage('zsh', '1', '3', None, 'i386')
        self.tsInfo.addUpdate(po, oldpo=ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po,))

    def testUpdateForDependency(self):
        po = FakePackage('zsh', '1', '1', '0', 'i386')
        po.addRequires('zip', 'EQ', ('0', '2', '1'))
        self.tsInfo.addInstall(po)

        installedpo = FakePackage('zip', '1', '1', '0', 'i386')
        self.rpmdb.addPackage(installedpo)

        updatepo = FakePackage('zip', '2', '1', '0', 'i386')
        self.xsack.addPackage(updatepo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, updatepo))

    def testUpdateSplitPackage(self):
        po = FakePackage('zsh', '1', '1', '0', 'i386')
        po.addRequires('libzip', 'EQ', ('0', '2', '1'))
        self.tsInfo.addInstall(po)

        installedpo = FakePackage('zip', '1', '1', '0', 'i386')
        installedpo.addProvides('libzip', 'EQ', ('0', '1', '1'))
        self.rpmdb.addPackage(installedpo)

        updatepo = FakePackage('zip', '2', '1', '0', 'i386')
        updatepo.addRequires('zip-libs', 'EQ', ('0', '2', '1'))
        self.xsack.addPackage(updatepo)
        updatepo2 = FakePackage('zip-libs', '2', '1', '0', 'i386')
        updatepo2.addProvides('libzip', 'EQ', ('0', '2', '1'))
        self.xsack.addPackage(updatepo2)

        self.assertEquals('ok', *self.resolveCode())
        #self.assertResult((po, updatepo, updatepo2)) # XXX obsolete needed?
        self.assertResult((po, installedpo, updatepo2))

    def testUpdateSinglePackageNewRequires(self):
        ipo = FakePackage('zsh', '1', '1', None, 'i386')
        self.rpmdb.addPackage(ipo)

        po = FakePackage('zsh', '1', '3', None, 'i386')
        po.addRequires('zip', None, (None, None, None))
        self.tsInfo.addUpdate(po, oldpo=ipo)

        xpo = FakePackage('zip', '1', '3', None, 'x86_64')
        self.xsack.addPackage(xpo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo))

    def testUpdateSinglePackageOldRequires(self):
        ipo = FakePackage('zsh', '1', '1', None, 'i386')
        ipo.addRequires('zip', None, (None, None, None))
        self.rpmdb.addPackage(ipo)

        xpo = FakePackage('zip', '1', '3', None, 'x86_64')
        self.rpmdb.addPackage(xpo)

        po = FakePackage('zsh', '1', '3', None, 'i386')
        po.addRequires('zip', None, (None, None, None))
        self.tsInfo.addUpdate(po, oldpo=ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo))

    def testUpdateSinglePackageOldRequiresGone(self):
        ipo = FakePackage('zsh', '1', '1', None, 'i386')
        ipo.addRequires('zip', None, (None, None, None))
        self.rpmdb.addPackage(ipo)

        xpo = FakePackage('zip', '1', '3', None, 'x86_64')
        self.rpmdb.addPackage(xpo)

        po = FakePackage('zsh', '1', '3', None, 'i386')
        self.tsInfo.addUpdate(po, oldpo=ipo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo))

    def testUpdateSinglePackageObsoletesOldRequirement(self):
        ipo = FakePackage('zsh', '1', '1', None, 'i386')
        ipo.addRequires('zip', None, (None, None, None))
        self.rpmdb.addPackage(ipo)

        opo = FakePackage('zip', '1', '1', None, 'i386')
        self.rpmdb.addPackage(opo)

        po = FakePackage('zsh', '1', '3', None, 'i386')
        ipo.addObsoletes('zip', None, (None, None, None))

        self.tsInfo.addUpdate(po, oldpo=ipo)

        self.tsInfo.addObsoleting(po, opo)
        self.tsInfo.addObsoleted(opo, po)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po,))

    def testUpdateForConflict(self):
        po = FakePackage('zsh', '1', '1', '0', 'i386')
        po.addConflicts('zip', 'LE', ('0', '1', '1'))
        self.tsInfo.addInstall(po)

        installedpo = FakePackage('zip', '1', '1', '0', 'i386')
        self.rpmdb.addPackage(installedpo)

        updatepo = FakePackage('zip', '2', '1', '0', 'i386')
        self.xsack.addPackage(updatepo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, updatepo))

    def testUpdateForConflict2(self):
        po = FakePackage('zsh', '1', '1', '0', 'i386')
        self.tsInfo.addInstall(po)

        installedpo = FakePackage('zip', '1', '1', '0', 'i386')
        installedpo.addConflicts('zsh', 'LE', ('0', '1', '1'))
        self.rpmdb.addPackage(installedpo)

        updatepo = FakePackage('zip', '2', '1', '0', 'i386')
        self.xsack.addPackage(updatepo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, updatepo))

    def testUpdateForConflictProvide(self):
        po = FakePackage('zsh', '1', '1', '0', 'i386')
        po.addConflicts('zippy', 'LE', ('0', '1', '1'))
        self.tsInfo.addInstall(po)

        installedpo = FakePackage('zip', '1', '1', '0', 'i386')
        installedpo.addProvides('zippy', 'EQ', ('0', '1', '1'))
        self.rpmdb.addPackage(installedpo)

        updatepo = FakePackage('zip', '2', '1', '0', 'i386')
        self.xsack.addPackage(updatepo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, updatepo))

    def testUpdateForConflictProvide2(self):
        po = FakePackage('zsh', '1', '1', '0', 'i386')
        po.addProvides('zippy', 'EQ', ('0', '2', '1'))
        self.tsInfo.addInstall(po)

        installedpo = FakePackage('zip', '1', '1', '0', 'i386')
        installedpo.addConflicts('zippy', 'GT', ('0', '1', '1'))
        installedpo.addConflicts('zippy', 'LT', ('0', '1', '1'))
        self.rpmdb.addPackage(installedpo)

        updatepo = FakePackage('zip', '2', '1', '0', 'i386')
        updatepo.addConflicts('zippy', 'GT', ('0', '2', '1'))
        updatepo.addConflicts('zippy', 'LT', ('0', '2', '1'))
        self.xsack.addPackage(updatepo)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, updatepo))

    def testEraseSinglePackage(self):
        po = FakePackage('zsh', '1', '1', '0', 'i386')
        self.rpmdb.addPackage(po)
        self.tsInfo.addErase(po)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult(())

    def testEraseSinglePackageRequiredByOneInstalled(self):
        po = FakePackage('zippy', '1', '1', '0', 'i386')
        po.addRequires('zsh', None, (None, None, None))
        self.rpmdb.addPackage(po)

        po = FakePackage('zsh', '1', '1', '0', 'i386')
        self.rpmdb.addPackage(po)
        self.tsInfo.addErase(po)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult(())

    def _setup_FakeMultilibReqs(self):
        po = FakePackage('abcd', '1', '0', '0', 'x86_64')
        po.addRequires('libxyz-1.so.0(64bit)', None, (None, None, None))
        po.addRequires('libxyz-1.so.0', None, (None, None, None))
        po.addRequires('libxyz-1.so.0(XYZ_1.1)(64bit)', None, (None,None,None))
        po.addRequires('libxyz-1.so.0(XYZ_1.2)(64bit)', None, (None,None,None))
        self.tsInfo.addInstall(po)

        xpo1 = FakePackage('libxyz', '1', '1', '0', 'x86_64')
        xpo1.addProvides('libxyz-1.so.0(64bit)', None,(None,None,None))
        xpo1.addProvides('libxyz-1.so.0(XYZ_1.1)(64bit)', None,(None,None,None))
        self.xsack.addPackage(xpo1)
        ipo1 = FakePackage('libxyz', '1', '1', '0', 'i386')
        ipo1.addProvides('libxyz-1.so.0', None,(None,None,None))
        ipo1.addProvides('libxyz-1.so.0(XYZ_1.1)', None,(None,None,None))
        self.xsack.addPackage(ipo1)
        xpo2 = FakePackage('libxyz', '1', '2', '0', 'x86_64')
        xpo2.addProvides('libxyz-1.so.0(64bit)', None,(None,None,None))
        xpo2.addProvides('libxyz-1.so.0(XYZ_1.1)(64bit)', None,(None,None,None))
        xpo2.addProvides('libxyz-1.so.0(XYZ_1.2)(64bit)', None,(None,None,None))
        self.xsack.addPackage(xpo2)
        ipo2 = FakePackage('libxyz', '1', '2', '0', 'i386')
        ipo2.addProvides('libxyz-1.so.0', None,(None,None,None))
        ipo2.addProvides('libxyz-1.so.0(XYZ_1.1)', None,(None,None,None))
        ipo2.addProvides('libxyz-1.so.0(XYZ_1.2)', None,(None,None,None))
        self.xsack.addPackage(ipo2)

        return (po, xpo1, xpo2, ipo1, ipo2)

    def testFakeMultilibReqsInstall(self):
        (po, xpo1, xpo2, ipo1, ipo2) = self._setup_FakeMultilibReqs()

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo2, ipo2))

    def testFakeMultilibReqsUpdate1a(self):
        (po, xpo1, xpo2, ipo1, ipo2) = self._setup_FakeMultilibReqs()
        self.rpmdb.addPackage(xpo1)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo2, ipo2))

    def testFakeMultilibReqsUpdate1b(self):
        (po, xpo1, xpo2, ipo1, ipo2) = self._setup_FakeMultilibReqs()
        self.rpmdb.addPackage(xpo1)
        # This doesn't suffer from the testFakeMultilibReqsUpdate1a()
        # problem because we have 2 32bit deps. ... and so the second one
        # wins.
        po.addRequires('libxyz-1.so.0(XYZ_1.1)', None, (None, None, None))

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo2, ipo2))

    def testFakeMultilibReqsUpdate2(self):
        (po, xpo1, xpo2, ipo1, ipo2) = self._setup_FakeMultilibReqs()
        self.rpmdb.addPackage(ipo1)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo2, ipo2))

    def testFakeMultilibReqsUpdate3(self):
        (po, xpo1, xpo2, ipo1, ipo2) = self._setup_FakeMultilibReqs()
        self.rpmdb.addPackage(xpo1)
        self.rpmdb.addPackage(ipo1)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, xpo2, ipo2))

    def _setup_CompareProviders(self, name="libbar", arch="x86_64"):
        po = FakePackage('abcd', arch=arch)
        po.addRequires('libxyz-1.so.0(64bit)', None, (None, None, None))
        self.tsInfo.addInstall(po)

        po1 = FakePackage('libfoo', arch=arch)
        po1.addProvides('libxyz-1.so.0(64bit)', None,(None,None,None))
        self.xsack.addPackage(po1)
        po2 = FakePackage(name, arch=arch)
        po2.addProvides('libxyz-1.so.0(64bit)', None,(None,None,None))
        self.xsack.addPackage(po2)
        return (po, po1, po2)

    def testCompareProviersSameLen1_64(self):
        (po, po1, po2) = self._setup_CompareProviders()

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po1))

    def testCompareProviersSameLen1_noarch(self):
        (po, po1, po2) = self._setup_CompareProviders(arch='noarch')

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po1))

    def testCompareProviersSameLen2_64(self):
        # Make sure they are still ok, the other way around
        po = FakePackage('abcd', arch='x86_64')
        po.addRequires('libxyz-1.so.0(64bit)', None, (None, None, None))
        self.tsInfo.addInstall(po)

        po2 = FakePackage('libbar', arch='x86_64')
        po2.addProvides('libxyz-1.so.0(64bit)', None,(None,None,None))
        self.xsack.addPackage(po2)
        po1 = FakePackage('libfoo', arch='x86_64')
        po1.addProvides('libxyz-1.so.0(64bit)', None,(None,None,None))
        self.xsack.addPackage(po1)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po1))

    def testCompareProviersSameLen2_noarch(self):
        # Make sure they are still ok, the other way around
        po = FakePackage('abcd', arch='noarch')
        po.addRequires('libxyz-1.so.0', None, (None, None, None))
        self.tsInfo.addInstall(po)

        po2 = FakePackage('libbar', arch='noarch')
        po2.addProvides('libxyz-1.so.0', None,(None,None,None))
        self.xsack.addPackage(po2)
        po1 = FakePackage('libfoo', arch='noarch')
        po1.addProvides('libxyz-1.so.0', None,(None,None,None))
        self.xsack.addPackage(po1)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po1))

    def testCompareProviersSameLen2_noarch_to_64_1(self):
        # Make sure they are still ok, the other way around
        po = FakePackage('abcd', arch='noarch')
        po.addRequires('libxyz-1.so.0', None, (None, None, None))
        self.tsInfo.addInstall(po)

        po2 = FakePackage('libbar', arch='i386')
        po2.addProvides('libxyz-1.so.0', None,(None,None,None))
        self.xsack.addPackage(po2)
        po1 = FakePackage('libfoo', arch='x86_64')
        po1.addProvides('libxyz-1.so.0', None,(None,None,None))
        self.xsack.addPackage(po1)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po1))

    def testCompareProviersSameLen2_noarch_to_64_2(self):
        # Make sure they are still ok, the other way around
        po = FakePackage('abcd', arch='noarch')
        po.addRequires('libxyz-1.so.0', None, (None, None, None))
        self.tsInfo.addInstall(po)

        po2 = FakePackage('libbar', arch='x86_64')
        po2.addProvides('libxyz-1.so.0', None,(None,None,None))
        self.xsack.addPackage(po2)
        po1 = FakePackage('libfoo', arch='i386')
        po1.addProvides('libxyz-1.so.0', None,(None,None,None))
        self.xsack.addPackage(po1)

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po2))

    def testCompareProviersDiffLen_64(self):
        (po, po1, po2) = self._setup_CompareProviders(name='libbarf')

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po1))

    def testCompareProviersDiffLen_noarch(self):
        (po, po1, po2) = self._setup_CompareProviders(name='libbarf',
                                                      arch='noarch')

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po1))

    def testCompareProviersSrcRpm_64(self):
        (po, po1, po2) = self._setup_CompareProviders(name='libbarf')
        po.sourcerpm  = "abcd.src.rpm"
        po2.sourcerpm = "abcd.src.rpm"

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po2))

    def testCompareProviersSrcRpm_noarch(self):
        (po, po1, po2) = self._setup_CompareProviders(name='libbarf',
                                                      arch='noarch')
        po.sourcerpm  = "abcd.src.rpm"
        po2.sourcerpm = "abcd.src.rpm"

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po2))

    def testCompareProviersPrefix_64(self):
        (po, po1, po2) = self._setup_CompareProviders(name='abcd-libbarf')

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po2))

    def testCompareProviersPrefix_noarch(self):
        (po, po1, po2) = self._setup_CompareProviders(name='abcd-libbarf',
                                                      arch='noarch')

        self.assertEquals('ok', *self.resolveCode())
        self.assertResult((po, po2))
