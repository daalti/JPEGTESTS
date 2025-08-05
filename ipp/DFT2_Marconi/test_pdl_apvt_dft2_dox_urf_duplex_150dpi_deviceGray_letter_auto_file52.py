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
    +external_files:printfile52.urf=5f9bdfe8d3f056ee3d15109f57664d3edc4da109637b72110de10378451ead12
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_duplex_150dpi_deviceGray_letter_auto_file52
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_duplex_150dpi_deviceGray_letter_auto_file52
        +guid:95f004f1-f87a-44c5-8a63-59d120446204
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_duplex_150dpi_deviceGray_letter_auto_file52(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_duplex_150dpi_deviceGray_letter_auto_file52.test', '5f9bdfe8d3f056ee3d15109f57664d3edc4da109637b72110de10378451ead12')
    outputsaver.save_output()
