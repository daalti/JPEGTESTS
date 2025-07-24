import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_hpgltopjl.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-hpgltopjl.obj=864e0e57de7fad63fa3b3268b9a3caeb3f375d50a75e800accaaa02a2bbb5aae
    +test_classification:System
    +name: test_pcl5_highvalue_1page_hpgltopjl
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_1page_hpgltopjl
        +guid:2c703f77-c744-4dce-9879-b3b1c5c73755
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

def test_pcl5_highvalue_1page_hpgltopjl(setup_teardown, printjob, outputsaver):
    printjob.print_verify('864e0e57de7fad63fa3b3268b9a3caeb3f375d50a75e800accaaa02a2bbb5aae',expected_jobs=2)
    outputsaver.save_output()
