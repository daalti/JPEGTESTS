import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 8Page_bestfit.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:8Page-bestfit.obj=6bb775b5eab406b931ecaa3d035f820a036db1f197d58b285f10d35fd94a1fe1
    +test_classification:System
    +name: test_pcl5_highvalue_8page_bestfit
    +test:
        +title: test_pcl5_highvalue_8page_bestfit
        +guid:7ae0d462-58a7-45e1-9323-cfa1d57d88cb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_8page_bestfit(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6bb775b5eab406b931ecaa3d035f820a036db1f197d58b285f10d35fd94a1fe1')
    outputsaver.save_output()
