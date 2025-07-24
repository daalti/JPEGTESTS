import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using ft_20_let.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:ft_20_let.pcl=b53ad4d0ea35b37d62874975649d0e83019b2c540ffd5d00c1887a460cd416cc
    +test_classification:System
    +name: test_pcl5_testfiles_whql_ft_20_let
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_whql_ft_20_let
        +guid:a19085ff-738a-403a-af8f-74d620041c62
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_whql_ft_20_let(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b53ad4d0ea35b37d62874975649d0e83019b2c540ffd5d00c1887a460cd416cc', timeout=600)
    outputsaver.save_output()
