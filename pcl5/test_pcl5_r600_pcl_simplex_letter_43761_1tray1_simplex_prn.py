import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:R600_pcl_Simplex_letter_43761-1Tray1_Simplex.prn=cea8434052273b26c90bf45289f9f7d2410136b02a8e7eb28dd4776ea60e9f40
    +name:test_pcl5_r600_pcl_simplex_letter_43761_1tray1_simplex_prn
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_r600_pcl_simplex_letter_43761_1tray1_simplex_prn
        +guid:3145f830-ab28-4519-803b-bc889c8fde6c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_r600_pcl_simplex_letter_43761_1tray1_simplex_prn(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('cea8434052273b26c90bf45289f9f7d2410136b02a8e7eb28dd4776ea60e9f40')
    outputsaver.save_output()                
