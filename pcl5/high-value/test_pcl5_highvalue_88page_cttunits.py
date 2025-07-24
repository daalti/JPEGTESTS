import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 88Page_cttunits.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1620
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:88Page-cttunits.obj=e6b14fb1424360bbceb60e2286012165ea387727bae009a1b90a2c0e7f6e219d
    +test_classification:System
    +name: test_pcl5_highvalue_88page_cttunits
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_88page_cttunits
        +guid:d1f1dc40-77b1-4656-88dd-561e173165e9
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

def test_pcl5_highvalue_88page_cttunits(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('e6b14fb1424360bbceb60e2286012165ea387727bae009a1b90a2c0e7f6e219d', timeout=1200,expected_jobs=3)
    outputsaver.save_output()
