import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 8Page_qp60gc01.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:8Page-qp60gc01.obj=a549a8efd2bd5544495eef61a6145ebdef0947823e1306a719dd80058c32980a
    +test_classification:System
    +name: test_pcl5_highvalue_8page_qp60gc01
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_8page_qp60gc01
        +guid:be10ec50-5753-4000-a81e-9c2f8c4d9fd6
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

def test_pcl5_highvalue_8page_qp60gc01(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a549a8efd2bd5544495eef61a6145ebdef0947823e1306a719dd80058c32980a',expected_jobs=3)
    outputsaver.save_output()
