import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 6Page_ffsuppress.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:400
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:6Page-ffsuppress.obj=4ee42ac716d7ce57d2855a7163d0d58a5fae6144ed60b864538a7f41d70dbe89
    +test_classification:System
    +name: test_pcl5_highvalue_6page_ffsuppress
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_6page_ffsuppress
        +guid:f6c3362d-16d5-4e50-af4c-ff412730ca93
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

def test_pcl5_highvalue_6page_ffsuppress(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')
    printjob.print_verify_multi('4ee42ac716d7ce57d2855a7163d0d58a5fae6144ed60b864538a7f41d70dbe89', timeout=400,expected_jobs=6)
    outputsaver.save_output()