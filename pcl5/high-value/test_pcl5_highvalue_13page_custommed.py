import pytest
import logging
from dunetuf.print.output.intents import Intents

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 13Page_custommed.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:13Page-custommed.obj=5423a3115ab10bbdbb589f019f55addfdf5c0d0be1955fd3be7f4c0eb79fc6e7
    +test_classification:System
    +name: test_pcl5_highvalue_13page_custommed
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_13page_custommed
        +guid:a7dd3104-277c-46c6-a97e-5897239453f6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 &  MediaSizeSupported=Any

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_13page_custommed(setup_teardown, printjob, outputsaver,tray,outputverifier):
    printjob.print_verify('5423a3115ab10bbdbb589f019f55addfdf5c0d0be1955fd3be7f4c0eb79fc6e7', timeout=300)
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 29)