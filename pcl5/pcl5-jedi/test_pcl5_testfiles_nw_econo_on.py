import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using nw_econo_on.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:nw_econo_on.pcl=adadb5b11f2675120e9a1ea8eef0ff696b819912f87a471ca1fdbbc2aeaa9a2c
    +test_classification:System
    +name: test_pcl5_testfiles_nw_econo_on
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_nw_econo_on
        +guid:59dfb3ce-163f-45e6-a52e-0ec513e9a969
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_nw_econo_on(setup_teardown, printjob, outputsaver):
    printjob.print_verify('adadb5b11f2675120e9a1ea8eef0ff696b819912f87a471ca1fdbbc2aeaa9a2c', timeout=600)
    outputsaver.save_output()
