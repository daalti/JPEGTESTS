import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using ch20_let.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:ch20_let.pcl=96cc3d100f83f028cf5f11007650af16d1a7ecaf306793c59fdf7e4f912caf2b
    +test_classification:System
    +name: test_pcl5_testfiles_whql_ch20_let
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_whql_ch20_let
        +guid:f82f97a3-4eb8-405e-a705-b054e199a96d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_whql_ch20_let(setup_teardown, printjob, outputsaver):
    printjob.print_verify('96cc3d100f83f028cf5f11007650af16d1a7ecaf306793c59fdf7e4f912caf2b', timeout=600)
    outputsaver.save_output()
