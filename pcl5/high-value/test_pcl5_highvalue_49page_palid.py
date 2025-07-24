import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30474186 pcl5 highvalue using 49Page_palid.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:49Page-palid.obj=f742ce064c1532b387821d7dd7ad99a339e2e8bf2667c45c24d8f66461e2d557
    +test_classification:System
    +name: test_pcl5_highvalue_49page_palid
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_49page_palid
        +guid:8d6006c2-3455-4b99-ac73-39645e7d81b6
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

def test_pcl5_highvalue_49page_palid(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f742ce064c1532b387821d7dd7ad99a339e2e8bf2667c45c24d8f66461e2d557', timeout=600)
    outputsaver.save_output()
