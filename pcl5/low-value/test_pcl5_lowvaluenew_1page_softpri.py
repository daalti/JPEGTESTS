import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 1Page_softpri.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-softpri.obj=35a24e12de49c3b1def1e36b30562bc06fd04bf6d007f8ea36b0207362e5744d
    +test_classification:System
    +name: test_pcl5_lowvaluenew_1page_softpri
    +test:
        +title: test_pcl5_lowvaluenew_1page_softpri
        +guid:f2ca68df-3567-4ed2-95d4-e48f8ff658af
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_1page_softpri(setup_teardown, printjob, outputsaver):
    printjob.print_verify('35a24e12de49c3b1def1e36b30562bc06fd04bf6d007f8ea36b0207362e5744d', timeout=600)
    outputsaver.save_output()
