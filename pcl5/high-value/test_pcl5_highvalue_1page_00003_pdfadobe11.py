import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_00003_PDFAdobe11.prn
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-00003_PDFAdobe11.prn=d3c9a33f4f43965629f9a8e10ac989d86aa98f1c552c502783f656935dfea40d
    +test_classification:System
    +name: test_pcl5_highvalue_1page_00003_pdfadobe11
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_1page_00003_pdfadobe11
        +guid:08384fff-b1a4-4235-be4d-f48a2a9394c5
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

def test_pcl5_highvalue_1page_00003_pdfadobe11(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d3c9a33f4f43965629f9a8e10ac989d86aa98f1c552c502783f656935dfea40d')
    outputsaver.save_output()
