import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using fnt8_let.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:fnt8_let.pcl=fa4f698d8dac15894a68f9cd7765e3a91ffa0c03181d932095a9a7a87683facf
    +test_classification:System
    +name: test_pcl5_testfiles_whql_fnt8_let
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_whql_fnt8_let
        +guid:8f578974-8660-4130-9dbc-85d35fa86647
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_whql_fnt8_let(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fa4f698d8dac15894a68f9cd7765e3a91ffa0c03181d932095a9a7a87683facf', timeout=600)
    outputsaver.save_output()
