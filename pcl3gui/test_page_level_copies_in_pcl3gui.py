import pytest
import logging

from dunetuf.print.output.intents import Intents

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PageCopies PJL support for SmartStream jobs
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-130648
    +timeout:600
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:page1_5copies_page1_1copy.pcl=c3b41ca0c4f8b2610b4a2432517a39afc86fa6b870ddb9c6d2ca5d7277f65e83
    +name:test_page_level_copies_in_pcl3gui
    +test:
        +title:test_page_level_copies_in_pcl3gui
        +guid:94d6377e-3563-4894-a3c7-777976fe792a
        +dut:
            +type:Simulator
            +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI & Print=NumberOfCopies
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_page_level_copies_in_pcl3gui(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('CRC')
    #The test file changed because previous test file expected unsupported media type on Jupiter & a prompt used to cause timeout
    #Modified the previous file by updating the media type to bond(Id: 1)
    printjob.print_verify('c3b41ca0c4f8b2610b4a2432517a39afc86fa6b870ddb9c6d2ca5d7277f65e83', timeout=600)
    expected_crc = ['0x2d0a4932', '0xb8e7ab58', '0xb8e7ab58', '0xb8e7ab58', '0xb8e7ab58', '0xb8e7ab58']

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)

    outputsaver.operation_mode('NONE')