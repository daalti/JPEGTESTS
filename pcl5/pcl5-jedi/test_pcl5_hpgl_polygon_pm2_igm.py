import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pm2_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pm2_igm.obj=fa68643ca10bc3edc453b95d0f2d560335b351fa36ef26fd258ac21854ab7e87
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_pm2_igm
    +test:
        +title: test_pcl5_hpgl_polygon_pm2_igm
        +guid:3b77ff30-80da-47fb-a83c-1c7c3cb301fd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_pm2_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fa68643ca10bc3edc453b95d0f2d560335b351fa36ef26fd258ac21854ab7e87', timeout=600)
    outputsaver.save_output()
