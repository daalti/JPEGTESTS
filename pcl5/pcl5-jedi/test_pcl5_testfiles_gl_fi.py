import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using fi.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fi.pcl=920c38d27b4095209fefc41982f2f9902014fcf602d4ba7231fb9ed3a648e14f
    +test_classification:System
    +name: test_pcl5_testfiles_gl_fi
    +test:
        +title: test_pcl5_testfiles_gl_fi
        +guid:bc3fafd5-664a-44bd-bad7-5d4121db8b81
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_fi(setup_teardown, printjob, outputsaver):
    printjob.print_verify('920c38d27b4095209fefc41982f2f9902014fcf602d4ba7231fb9ed3a648e14f', timeout=600)
    outputsaver.save_output()
