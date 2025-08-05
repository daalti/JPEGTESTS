import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile65.urf=5f935e756d3177e8fd511f343f7b14d936556fc2d1e8784d763f344336aafe0f
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_Gray_Duplex_RGB_Gray_letter_auto_file66
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_Gray_Duplex_RGB_Gray_letter_auto_file66
        +guid:08810467-ded9-4e01-87f6-e64566b1e4f7
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_Gray_Duplex_RGB_Gray_letter_auto_file66(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_Gray_Duplex_RGB_Gray_letter_auto_file66.test', '5f935e756d3177e8fd511f343f7b14d936556fc2d1e8784d763f344336aafe0f')
    outputsaver.save_output()
