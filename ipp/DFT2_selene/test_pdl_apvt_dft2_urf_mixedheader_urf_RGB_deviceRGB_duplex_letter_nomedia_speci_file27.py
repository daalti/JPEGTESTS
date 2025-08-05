import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile25.urf=e97b7f522afbff92835f33d5f36be8e058dc4ec36456414195155f16f8da00e5
    +test_classification:System
    +name:test_pdl_apvt_dft2_urf_mixedheader_RGB_deviceRGB_duplex_letter_nomedia_speci_file27
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_urf_mixedheader_RGB_deviceRGB_duplex_letter_nomedia_speci_file27
        +guid:daa911f5-c74f-4747-a714-eae1d855e94a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_urf_mixedheader_RGB_deviceRGB_duplex_letter_nomedia_speci_file27(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_urf_mixedheader_RGB_deviceRGB_duplex_letter_nomedia_speci_file27.test', 'e97b7f522afbff92835f33d5f36be8e058dc4ec36456414195155f16f8da00e5')
    outputsaver.save_output()