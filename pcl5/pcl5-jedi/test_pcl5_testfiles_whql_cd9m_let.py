import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using Cd9m_let.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:800
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:Cd9m_let.pcl=2c5274e74f1e7bf4fe0fcd5bc27e954e5f364e81e6e0a7871c9f9d1bf6e6ab83
    +test_classification:System
    +name: test_pcl5_testfiles_whql_cd9m_let
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_whql_cd9m_let
        +guid:7129d6f1-089a-4f7e-975d-4e098a9c4418
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_testfiles_whql_cd9m_let(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2c5274e74f1e7bf4fe0fcd5bc27e954e5f364e81e6e0a7871c9f9d1bf6e6ab83', timeout=600)
    outputsaver.save_output()
