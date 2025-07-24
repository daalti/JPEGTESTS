import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using AlphaDiskFonts.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:AlphaDiskFonts.pcl=3221363305f63378a5e734ab919ca040c960847f804be5bf46d6176b085adf67
    +test_classification:System
    +name: test_pcl5_testfiles_misc_alphadiskfonts
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_misc_alphadiskfonts
        +guid:b627aa8b-5a0a-46bb-9d68-8f1b29da8739
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_alphadiskfonts(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3221363305f63378a5e734ab919ca040c960847f804be5bf46d6176b085adf67', timeout=600)
    outputsaver.save_output()
