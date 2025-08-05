import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile28.urf=1781be6a147c7704be8cb82d143ea4c814c32b3cd261f565ff5c3305a00dfdd0
    +test_classification:System
    +name:test_pdl_apvt_dft2_urf_mixedheader_deviceRGB_device_gray_duplex_nomedia_speci_file29
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_urf_mixedheader_deviceRGB_device_gray_duplex_nomedia_speci_file29
        +guid:b4b93534-0879-45ca-9000-72f6deae7d53
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_urf_mixedheader_deviceRGB_device_gray_duplex_nomedia_speci_file29(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_urf_mixedheader_deviceRGB_devicegray_duplex_nomedia_speci_file29.test', '1781be6a147c7704be8cb82d143ea4c814c32b3cd261f565ff5c3305a00dfdd0')
    outputsaver.save_output()