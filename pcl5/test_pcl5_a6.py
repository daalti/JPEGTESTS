import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464	
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:a6.pcl=dc0d40eb3bce9b392efecd10234a0fb2ef0449e879cf5e918abff5cb3fb617c5
    +name:test_pcl5_a6
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_a6
        +guid:8e12b7e0-4dc3-4aec-8ef1-4695e133d891
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5
    +overrides:
        +Home:
            +is_manual:False
            +timeout:240
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_a6(setup_teardown, printjob, outputsaver,tray):
    if tray.is_size_supported('iso_a6_105x148mm','tray-1'):
        tray.configure_tray('tray-1', 'iso_a6_105x148mm', 'any')
    printjob.print_verify_multi('dc0d40eb3bce9b392efecd10234a0fb2ef0449e879cf5e918abff5cb3fb617c5', timeout=200)
    outputsaver.save_output()