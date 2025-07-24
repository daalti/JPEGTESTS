import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using nw_econo_off.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:nw_econo_off.pcl=9ed1a5a8c18838ae6ad6788c4e79a1ec95c7fff8ec3e9ce2ca8984103ba0d458
    +test_classification:System
    +name: test_pcl5_testfiles_nw_econo_off
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_nw_econo_off
        +guid:15bd856c-f6f9-426a-9880-0fa78dfdf50c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_nw_econo_off(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9ed1a5a8c18838ae6ad6788c4e79a1ec95c7fff8ec3e9ce2ca8984103ba0d458', timeout=600)
    outputsaver.save_output()
