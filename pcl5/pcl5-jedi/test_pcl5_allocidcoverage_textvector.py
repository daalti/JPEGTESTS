import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 allocidcoverage using TextVector.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:TextVector.pcl=ce90331a6a06cad7c333d480eb14a347d5b17d3c525ac73f5968064b96d15eac
    +test_classification:System
    +name: test_pcl5_allocidcoverage_textvector
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_allocidcoverage_textvector
        +guid:0468b1ad-db3f-401e-8424-f19d02871daa
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""



def test_pcl5_allocidcoverage_textvector(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ce90331a6a06cad7c333d480eb14a347d5b17d3c525ac73f5968064b96d15eac', timeout=600)
    outputsaver.save_output()
