import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pm_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pm_igm.obj=aef1f37f4f39331731ba6c294403201e4ee7672c07934709fdb42af039f185e0
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_pm_igm
    +test:
        +title: test_pcl5_hpgl_polygon_pm_igm
        +guid:db250775-cae6-4f2e-bada-32a9f8a52a28
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_pm_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('aef1f37f4f39331731ba6c294403201e4ee7672c07934709fdb42af039f185e0', timeout=600)
    outputsaver.save_output()
