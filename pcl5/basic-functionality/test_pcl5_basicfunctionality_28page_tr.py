import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 28Page_tr.obj
    +test_tier: 3
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:28Page-tr.obj=48c316d47d51b129d88afacbec6a28dac2f672f9ffd516bc45ad5b30408628f7
    +test_classification:System
    +name: test_pcl5_basicfunctionality_28page_tr
    +test:
        +title: test_pcl5_basicfunctionality_28page_tr
        +guid:769eea1d-9cc4-4a87-8b4b-80b35a3940d1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_28page_tr(setup_teardown, printjob, outputsaver):
    printjob.print_verify('48c316d47d51b129d88afacbec6a28dac2f672f9ffd516bc45ad5b30408628f7',timeout =240)
    outputsaver.save_output()
