import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464
    +timeout:500
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:officio.prn=9fa4f8ad2821d45fa54ca21eb3f94fc75ac56e58d39ebf2ba6127a72bd3723e5
    +name:test_pcl5_officio_prn
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_officio_prn
        +guid:5aa9744a-9d03-4bea-a8be-ad884feb2393
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_officio_prn(setup_teardown, printjob, outputsaver,tray):
    if tray.is_size_supported('na_foolscap_8.5x13in','tray-1'):
        tray.configure_tray('tray-1', 'na_foolscap_8.5x13in', 'any')
    printjob.print_verify_multi('9fa4f8ad2821d45fa54ca21eb3f94fc75ac56e58d39ebf2ba6127a72bd3723e5',timeout=500)
    outputsaver.save_output()