#ifndef DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_LARGE_FORMAT_MAPPER_H
#define DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_LARGE_FORMAT_MAPPER_H
///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesLargeFormatMapper.h
 * @date   Tue, 11 Oct 2022 11:20:06 +0200
 * @brief  Namespace with maps between types and main method executions
 * @author yago.cordero.carrera@hp.com (Cordero Carrera, Yago)
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////
#include <unordered_map>
#include "CopyJobDynamicConstraintRulesLargeFormatConfig_generated.h"
#include "com.hp.cdm.service.jobTicket.version.1.easybuffers_autogen.h"
#include "CopyJobTicket.h"
#include "typeMappers.h"
#include "MediaCdmHelper.h"
#include "Constraints.h"
#include "ValidValues.h"
#include "MinLength.h"
#include "MaxLength.h"
#include "Range.h"
#include "com.hp.cdm.service.jobTicket.version.1.easybuffers_autogen.h"

using dune::cdm::jobTicket_1::JobTicketTable;
namespace dune { namespace copy { namespace Jobs { namespace Copy {
namespace CopyJobDynamicConstraintRulesLargeFormatMapperLogger
{
    /**
     * @brief Method to write to log a debug message     
     * @param message to be written     
     */
    void checkpointDebug(const char* message);

    /**
     * @brief Method to write to log an info message
     * @param message to be written     
     */
    void checkpointInfo(const char* message);

    /**
     * @brief Method to write to log a warning message
     * @param message to be written     
     */
    void checkpointWarning(const char* message);
};

/**
 * @brief Namespace to encapsulate mapper checker for parser ticket method 
 */
namespace Map2CheckerTicketMethod
{
    /**
     * @brief Method to check if a intent value union has the expected needed type     
     * @param value current value to check
     * @param type type expected
     */
    inline void checkValueType(CopyIntentValuesUnion value,CopyIntentValues type)
    {
        assert_msg(value.type == type,"Typo of CopyIntentValuesUnion not coincidence with the expected");
    }

    // * Getter Value Union from Copy Intent Value Union Table
    /**
     * @brief Parse a Intent Value Union to expected cdm value     
     * @tparam CdmType template to indicate type for cdm
     * @param value union value from flatbuffer
     * @return CdmType cdm type result
     */
    template<typename TypeFromUnion>
    inline TypeFromUnion getValue(CopyIntentValuesUnion value);

    // Different getters execution. 
    // ? Add new method here if there is any missed item parsing that is need to be supported

    // Specific tables 
    template<>
    inline dune::copy::Jobs::Copy::MinMaxLengthUIntT* getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsMinMaxLengthUInt() != nullptr,"Not MinMaxLengthUInt value, unsupported getter");
        return value.AsMinMaxLengthUInt();
    }

    template<>
    inline dune::copy::Jobs::Copy::TEXTT* getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsTEXT() != nullptr,"Not TEXT value, unsupported getter");
        return value.AsTEXT();
    }

    template<>
    inline dune::copy::Jobs::Copy::RangeValueIntT* getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsRangeValueInt() != nullptr,"Not RangeValueInt value, unsupported getter");
        return value.AsRangeValueInt();
    }

    template<>
    inline dune::copy::Jobs::Copy::RangeValueDoubleT* getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsRangeValueDouble() != nullptr,"Not RangeValueDouble value, unsupported getter");
        return value.AsRangeValueDouble();
    }

    // Basic Types
    template<>
    inline int8_t getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsINT8() != nullptr,"Not INT8 value, unsupported getter");
        return value.AsINT8()->value;
    }

    template<>
    inline int16_t getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsINT16() != nullptr,"Not INT16 value, unsupported getter");
        return value.AsINT16()->value;
    }

    template<>
    inline int32_t getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsINT32() != nullptr,"Not INT32 value, unsupported getter");
        return value.AsINT32()->value;
    }

    template<>
    inline int64_t getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsINT64() != nullptr,"Not INT64 value, unsupported getter");
        return value.AsINT64()->value;
    }

    template<>
    inline uint8_t getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsUINT8() != nullptr,"Not INT8 value, unsupported getter");
        return value.AsUINT8()->value;
    }

    template<>
    inline uint16_t getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsUINT16() != nullptr,"Not INT16 value, unsupported getter");
        return value.AsUINT16()->value;
    }

    template<>
    inline uint32_t getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsUINT32() != nullptr,"Not INT32 value, unsupported getter");
        return value.AsUINT32()->value;
    }

    template<>
    inline uint64_t getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsUINT64() != nullptr,"Not INT64 value, unsupported getter");
        return value.AsUINT64()->value;
    }

    template<>
    inline double getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsDOUBLE() != nullptr,"Not double value, unsupported getter");
        return value.AsDOUBLE()->value;
    }

    template<>
    inline bool getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsBOOL() != nullptr,"Not BOOL value, unsupported getter");
        return value.AsBOOL()->value;
    }

    template<>
    inline dune::scan::types::AttachmentSize getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsAttachmentSize() != nullptr,"Not AttachmentSize value, unsupported getter");
        return value.AsAttachmentSize()->value;
    }

    template<>
    inline dune::scan::types::OriginalMediaType getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsOriginalMediaType() != nullptr,"Not OriginalMediaType value, unsupported getter");
        return value.AsOriginalMediaType()->value;
    }
         
    template <>
    inline dune::scan::types::ScanSource getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsScanSource() != nullptr,"Not ScanSource value, unsupported getter");
        return value.AsScanSource()->value;
    }

    template <>
    inline dune::scan::types::ScanFeedOrientation getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsScanFeedOrientation() != nullptr,"Not ScanFeedOrientation value, unsupported getter");
        return value.AsScanFeedOrientation()->value;
    }

    template <>
    inline dune::scan::types::BlankDetectEnum getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsBlankDetectEnum() != nullptr,"Not BlankDetectEnum value, unsupported getter");
        return value.AsBlankDetectEnum()->value;
    }

    template <>
    inline dune::scan::types::OverScanType getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsOverScanType() != nullptr,"Not OverScanType value, unsupported getter");
        return value.AsOverScanType()->value;
    }

    template <>
    inline dune::scan::types::ScanCaptureModeType getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsScanCaptureModeType() != nullptr,"Not ScanCaptureModeType value, unsupported getter");
        return value.AsScanCaptureModeType()->value;
    }

    template <>
    inline dune::scan::types::ScanImagingProfileType getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsScanImagingProfileType() != nullptr,"Not ScanImagingProfileType value, unsupported getter");
        return value.AsScanImagingProfileType()->value;
    }

    template <>
    inline dune::scan::types::CcdChannelEnum getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsCcdChannelEnum() != nullptr,"Not CcdChannelEnum value, unsupported getter");
        return value.AsCcdChannelEnum()->value;
    }

    template <>
    inline dune::scan::types::BinaryRenderingEnum getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsBinaryRenderingEnum() != nullptr,"Not BinaryRenderingEnum value, unsupported getter");
        return value.AsBinaryRenderingEnum()->value;
    }

    template <>
    inline dune::scan::types::AutoColorDetectEnum getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsAutoColorDetectEnum() != nullptr,"Not AutoColorDetectEnum value, unsupported getter");
        return value.AsAutoColorDetectEnum()->value;
    }

    template <>
    inline dune::scan::types::ImagePreview getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsImagePreview() != nullptr,"Not ImagePreview value, unsupported getter");
        return value.AsImagePreview()->value;
    }

    template <>
    inline dune::scan::types::ScanScaleSelectionEnum getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsScanScaleSelectionEnum() != nullptr,"Not ScanScaleSelectionEnum value, unsupported getter");
        return value.AsScanScaleSelectionEnum()->value;
    }

    template <>
    inline dune::scan::types::ScanAcquisitionsSpeedEnum getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsScanAcquisitionsSpeedEnum() != nullptr,"Not ScanAcquisitionsSpeedEnum value, unsupported getter");
        return value.AsScanAcquisitionsSpeedEnum()->value;
    }

    template <>
    inline dune::imaging::types::ColorMode getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsColorMode() != nullptr,"Not ColorMode value, unsupported getter");
        return value.AsColorMode()->value;
    }

    template <>
    inline dune::imaging::types::ContentOrientation getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsContentOrientation() != nullptr,"Not ContentOrientation value, unsupported getter");
        return value.AsContentOrientation()->value;
    }

    template <>
    inline dune::imaging::types::OriginalContentType getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsOriginalContentType() != nullptr,"Not OriginalContentType value, unsupported getter");
        return value.AsOriginalContentType()->value;
    }

    template <>
    inline dune::imaging::types::MediaSizeId getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsMediaSizeId() != nullptr,"Not MediaSizeId value, unsupported getter");
        return value.AsMediaSizeId()->value;
    }

    template <>
    inline dune::imaging::types::PlexBinding getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsPlexBinding() != nullptr,"Not PlexBinding value, unsupported getter");
        return value.AsPlexBinding()->value;
    }

    template <>
    inline dune::imaging::types::Plex getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsPlex() != nullptr,"Not Plex value, unsupported getter");
        return value.AsPlex()->value;
    }

    template <>
    inline dune::imaging::types::Resolution getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsResolution() != nullptr,"Not Resolution value, unsupported getter");
        return value.AsResolution()->value;
    }

    template <>
    inline dune::imaging::types::MediaSource getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsMediaSource() != nullptr,"Not MediaSource value, unsupported getter");
        return value.AsMediaSource()->value;
    }

    template <>
    inline std::shared_ptr<dune::imaging::types::OutputCanvasT> getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsOutputCanvas() != nullptr,"Not OutputCanvas value, unsupported getter");
        return value.AsOutputCanvas()->value;
    }

    template <>
    inline dune::imaging::types::OutputCanvasAnchorType getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsOutputCanvasAnchorType() != nullptr,"Not OutputCanvasAnchorType value, unsupported getter");
        return value.AsOutputCanvasAnchorType()->value;
    }

    template <>
    inline dune::imaging::types::MediaOrientation getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsMediaOrientation() != nullptr,"Not MediaOrientation value, unsupported getter");
        return value.AsMediaOrientation()->value;
    }
    
    template <>
    inline dune::imaging::types::MediaIdType getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsMediaIdType() != nullptr,"Not MediaIdType value, unsupported getter");
        return value.AsMediaIdType()->value;
    }

    template <>
    inline dune::imaging::types::MediaDestinationId getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsMediaDestinationId() != nullptr,"Not MediaDestinationId value, unsupported getter");
        return value.AsMediaDestinationId()->value;
    }

    template <>
    inline dune::imaging::types::PrintQuality getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsPrintQuality() != nullptr,"Not PrintQuality value, unsupported getter");
        return value.AsPrintQuality()->value;
    }

    template <>
    inline dune::imaging::types::CopyOutputNumberUpCount getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsCopyOutputNumberUpCount() != nullptr,"Not CopyOutputNumberUpCount value, unsupported getter");
        return value.AsCopyOutputNumberUpCount()->value;
    }

    template <>
    inline dune::imaging::types::CopyMargins getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsCopyMargins() != nullptr,"Not CopyMargins value, unsupported getter");
        return value.AsCopyMargins()->value;
    }

    template <>
    inline dune::imaging::types::PrintingOrder getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsPrintingOrder() != nullptr,"Not PrintingOrder value, unsupported getter");
        return value.AsPrintingOrder()->value;
    }

    template <>
    inline dune::imaging::types::MediaFamily getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsMediaFamily() != nullptr,"Not MediaFamily value, unsupported getter");
        return value.AsMediaFamily()->value;
    }

    template <>
    inline dune::imaging::types::Rotate getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsRotate() != nullptr,"Not Rotate value, unsupported getter");
        return value.AsRotate()->value;
    }

    template <>
    inline dune::copy::SheetCollate getValue(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsSheetCollate() != nullptr,"Not SheetCollate value, unsupported getter");
        return value.AsSheetCollate()->value;
    }

    /**
     * @brief Unordered map to manage check between a CopyIntentValuesUnion with a ticket
     * 
     * string used as key, indicate the getter to ticket
     * 
     * ? If there is any setting not covered, add here.
     * ? Maintain a few the order of first scan settings, then part of copy-print.
     * ? Take care to add enum ticket setting on fbs if you need a new one.
     */
    static std::unordered_map<std::string, std::function<bool(CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket)>> MAP
    {         
        {
            "src/scan/mediaSize",                 
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSizeId);         
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSizeId>(value) == ticket->getIntent()->getInputMediaSizeId(); 
            }
        },
        {
            "src/scan/plexMode",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::Plex);                
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::Plex>(value) == ticket->getIntent()->getInputPlexMode();
            }
        },
        {
            "src/scan/resolution",               
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::Resolution);          
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::Resolution>(value) == ticket->getIntent()->getOutputXResolution();
            }
        },
        // Not currently supported
        // {
        //     "",            
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::AttachmentSize);      
        //         return Map2CheckerTicketMethod::getValue<dune::scan::types::AttachmentSize>(value) == ticket->getIntent()->getCopyQuality();
        //     }
        // },
        {
            "src/scan/colorMode",                       
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ColorMode);           
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::ColorMode>(value) == ticket->getIntent()->getColorMode();
            }
        },
        {
            "src/scan/contentOrientation",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ContentOrientation);  
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::ContentOrientation>(value) == ticket->getIntent()->getContentOrientation();
            }
        },
        // Not supported
        // {
        //     "",       
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ContentOrientation);  
        //         return Map2CheckerTicketMethod::getValue<dune::imaging::types::ContentOrientation>(value) == ticket->getIntent()->getBackSideContentOrientation();
        //     }
        // },
        {
            "src/scan/contentType",              
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::OriginalContentType); 
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::OriginalContentType>(value) == ticket->getIntent()->getOriginalContentType();
            }
        },
        {
            "src/scan/mediaType",                
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::OriginalMediaType);
                return Map2CheckerTicketMethod::getValue<dune::scan::types::OriginalMediaType>(value) == ticket->getIntent()->getOriginalMediaType();
            }
        },
        {
            "src/scan/mediaSource",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ScanSource);          
                return Map2CheckerTicketMethod::getValue<dune::scan::types::ScanSource>(value) == ticket->getIntent()->getScanSource();
            }
        },
        {
            "pipelineOptions/scaling/xScalePercent",                    
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT64);               
                return Map2CheckerTicketMethod::getValue<int64_t>(value) == ticket->getIntent()->getXScalePercent();
            }
        },
        {
            "pipelineOptions/scaling/yScalePercent",                   
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT64);               
                return Map2CheckerTicketMethod::getValue<int64_t>(value) == ticket->getIntent()->getYScalePercent();
            }
        },
        {
            "pipelineOptions/scaling/scaleToFitEnabled",               
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getScaleToFitEnabled();
            }
        },
        // Next are not supported
        // {
        //     "",              
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ScanFeedOrientation); 
        //         return Map2CheckerTicketMethod::getValue<dune::scan::types::ScanFeedOrientation>(value) == ticket->getIntent()->getScanFeedOrientation();
        //     }
        // },
        // {
        //     "",                  
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::Resolution);          
        //         return Map2CheckerTicketMethod::getValue<dune::imaging::types::Resolution>(value) == ticket->getIntent()->getScanXResolution();
        //     }
        // },
        // {
        //     "",                  
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::Resolution);          
        //         return Map2CheckerTicketMethod::getValue<dune::imaging::types::Resolution>(value) == ticket->getIntent()->getScanYResolution();
        //     }
        // },
        // {
        //     "",               
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
        //         return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getMultipickDetection();
        //     }
        // },
        // {
        //     "",                     
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);                 
        //         return Map2CheckerTicketMethod::getValue<int>(value) == ticket->getIntent()->getJobScanLimit();
        //     }
        // },
        // {
        //     "",                         
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
        //         return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getAutoCrop();
        //     }
        // },
        // {
        //     "",                         
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
        //         return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getAutoTone();
        //     }
        // },
        {
            "pipelineOptions/imageModifications/blankPageSuppressionEnabled",               
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BlankDetectEnum);     
                return Map2CheckerTicketMethod::getValue<dune::scan::types::BlankDetectEnum>(value) == ticket->getIntent()->getBlankPageDetection();
            }
        },
        {
            "pipelineOptions/imageModifications/exposure",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::UINT32);              
                return Map2CheckerTicketMethod::getValue<uint32_t>(value) == ticket->getIntent()->getBrightness();
            }
        },
        {
            "pipelineOptions/imageModifications/contrast",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::UINT32);              
                return Map2CheckerTicketMethod::getValue<uint32_t>(value) == ticket->getIntent()->getContrast();
            }
        },
        {
            "pipelineOptions/imageModifications/sharpness",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::UINT32);              
                return Map2CheckerTicketMethod::getValue<uint32_t>(value) == ticket->getIntent()->getSharpen();
            }
        },
        {
            "src/scan/xOffset",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::UINT32);              
                return Map2CheckerTicketMethod::getValue<uint32_t>(value) == ticket->getIntent()->getXOffset();
            }
        },
        {
            "src/scan/yOffset",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::UINT32);              
                return Map2CheckerTicketMethod::getValue<uint32_t>(value) == ticket->getIntent()->getYOffset();
            }
        },
        // Not supported
        // {
        //     "",                          
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::UINT32);              
        //         return Map2CheckerTicketMethod::getValue<uint32_t>(value) == ticket->getIntent()->getXExtend();
        //     }
        // },
        // {
        //     "",                          
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::UINT32);              
        //         return Map2CheckerTicketMethod::getValue<uint32_t>(value) == ticket->getIntent()->getYExtend();
        //     }
        // },
        {
            "pipelineOptions/imageModifications/backgroundCleanup",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::UINT32);              
                return Map2CheckerTicketMethod::getValue<uint32_t>(value) == ticket->getIntent()->getBackgroundRemoval();
            }
        },
        // {
        //     TicketSettingEnum::scanJobIntent_overScan,                         
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::OverScanType);        
        //         return Map2CheckerTicketMethod::getValue<dune::scan::types::OverScanType>(value) == ticket->getIntent()->getOverScan();
        //     }
        // },
        {
            "src/scan/scanCaptureMode",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ScanCaptureModeType); 
                return Map2CheckerTicketMethod::getValue<dune::scan::types::ScanCaptureModeType>(value) == ticket->getIntent()->getScanCaptureMode();
            }
        },
        // {
        //     TicketSettingEnum::scanJobIntent_scanImageProfile,                 
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ScanImagingProfileType); 
        //         return Map2CheckerTicketMethod::getValue<dune::scan::types::ScanImagingProfileType>(value) == ticket->getIntent()->getScanImagingProfile();
        //     }
        // },
        {
            "src/scan/ccdChannel",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::CcdChannelEnum);      
                return Map2CheckerTicketMethod::getValue<dune::scan::types::CcdChannelEnum>(value) == ticket->getIntent()->getCcdChannel();
            }
        },
        {
            "src/scan/binaryRendering",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BinaryRenderingEnum); 
                return Map2CheckerTicketMethod::getValue<dune::scan::types::BinaryRenderingEnum>(value) == ticket->getIntent()->getBinaryRendering();
            }
        },
        {
            "src/scan/descreen",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getDescreen();
            }
        },
        {
            "src/scan/feederPickStop",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getFeederPickStop();
            }
        },
        {
            "src/scan/shadow",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::UINT32);              
                return Map2CheckerTicketMethod::getValue<uint32_t>(value) == ticket->getIntent()->getShadow();
            }
        },
        {
            "src/scan/compressionFactor",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);                 
                return Map2CheckerTicketMethod::getValue<int>(value) == ticket->getIntent()->getCompressionFactor();
            }
        },
        {
            "src/scan/threshold",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::UINT32);              
                return Map2CheckerTicketMethod::getValue<uint32_t>(value) == ticket->getIntent()->getThreshold();
            }
        },
        {
            "src/scan/autoColorDetect",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::AutoColorDetectEnum); 
                return Map2CheckerTicketMethod::getValue<dune::scan::types::AutoColorDetectEnum>(value) == ticket->getIntent()->getScanAutoColorDetect();
            }
        },
        {
            "src/scan/blackBackground",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getScanBlackBackground();
            }
        },
        // {
        //     "",                  
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::UINT32);              
        //         return Map2CheckerTicketMethod::getValue<uint>(value) == ticket->getIntent()->getScanNumberPages();
        //     }
        // },
        {
            "src/scan/autoExposure",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getScanAutoExposure();
            }
        },
        {
            "src/scan/gamma",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::UINT32);              
                return Map2CheckerTicketMethod::getValue<uint>(value) == ticket->getIntent()->getScanGamma();
            }
        },
        {
            "src/scan/highlight",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);              
                return Map2CheckerTicketMethod::getValue<int32_t>(value) == ticket->getIntent()->getScanHighlight();
            }
        },
        {
            "src/scan/colorSensitivity",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);              
                return Map2CheckerTicketMethod::getValue<int32_t>(value) == ticket->getIntent()->getScanColorSensitivity();
            }
        },
        {
            "src/scan/colorRange",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);               
                return Map2CheckerTicketMethod::getValue<int>(value) == ticket->getIntent()->getScanColorRange();
            }
        },
        {
            "src/scan/pagesFlipUpEnabled",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getScanPagesFlipUpEnabled();
            }
        },
        {
            "pipelineOptions/manualUserOperations/imagePreviewConfiguration",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ImagePreview);        
                return Map2CheckerTicketMethod::getValue<dune::scan::types::ImagePreview>(value) == ticket->getIntent()->getImagePreview();
            }
        },
        {
            "pipelineOptions/imageModifications/pagesPerSheet",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::CopyOutputNumberUpCount); 
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::CopyOutputNumberUpCount>(value) == ticket->getIntent()->getPagesPerSheet();
            }
        },
        {
            "pipelineOptions/scaling/scaleSelection",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ScanScaleSelectionEnum); 
                return Map2CheckerTicketMethod::getValue<dune::scan::types::ScanScaleSelectionEnum>(value) == ticket->getIntent()->getScaleSelection();
            }
        },
        {
            "pipelineOptions/manualUserOperations/autoRelease",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getAutoRelease();
            }
        },
        {
            "src/scan/scanAcquisitionsSpeed",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ScanAcquisitionsSpeedEnum); 
                return Map2CheckerTicketMethod::getValue<dune::scan::types::ScanAcquisitionsSpeedEnum>(value) == ticket->getIntent()->getScanAcquisitionsSpeed();
            }
        },
        // {
        //     TicketSettingEnum::scanJobIntent_generatePreview,                  
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
        //         return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getGeneratePreview();
        //     }
        // },
        {
            "src/scan/autoDeskew",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getAutoDeskew();
            }
        },
        {
            "pipelineOptions/scaling/scaleToSize",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSizeId);
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSizeId>(value) == ticket->getIntent()->getScaleToSize();
            }
        },
        {
            "pipelineOptions/scaling/scaleToOutput",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSource);
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSource>(value) == ticket->getIntent()->getScaleToOutput();
            }
        },
        {
            "src/scan/edgeToEdgeScan",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getEdgeToEdgeScan();
            }
        },
        {
            "src/scan/longPlotScan",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getLongPlotScan();
            }
        },
        {
            "src/scan/invertColors",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getInvertColors();
            }
        },
        // {
        //     TicketSettingEnum::scanJobIntent_outputCanvas,                     
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::OutputCanvas);
        //         std::shared_ptr<dune::imaging::types::OutputCanvasT> unionValue = Map2CheckerTicketMethod::getValue<std::shared_ptr<dune::imaging::types::OutputCanvasT>>(value);

        //         bool checkResult =  (unionValue->outputCanvasMediaSize   == ticket->getIntent()->getOutputCanvas().outputCanvasMediaSize) && 
        //                             (unionValue->outputCanvasMediaId     == ticket->getIntent()->getOutputCanvas().outputCanvasMediaId) &&
        //                             (unionValue->outputCanvasXExtent     == ticket->getIntent()->getOutputCanvas().outputCanvasXExtent) &&
        //                             (unionValue->outputCanvasYExtent     == ticket->getIntent()->getOutputCanvas().outputCanvasYExtent) &&
        //                             (unionValue->outputCanvasAnchor      == ticket->getIntent()->getOutputCanvas().outputCanvasAnchor) &&
        //                             (unionValue->outputCanvasOrientation == ticket->getIntent()->getOutputCanvas().outputCanvasOrientation);

        //         return checkResult;
        //     }
        // },
        {
            "pipelineOptions/imageModifications/outputCanvasMediaSize",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSizeId);
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSizeId>(value) == ticket->getIntent()->getOutputCanvas().outputCanvasMediaSize;
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasMediaId",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSource);
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSource>(value) == ticket->getIntent()->getOutputCanvas().outputCanvasMediaId;
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasCustomWidth",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::DOUBLE);
                return Map2CheckerTicketMethod::getValue<double>(value) == ticket->getIntent()->getOutputCanvas().outputCanvasXExtent;
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasCustomLength",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::DOUBLE);              
                return Map2CheckerTicketMethod::getValue<double>(value) == ticket->getIntent()->getOutputCanvas().outputCanvasYExtent;
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasAnchor",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::OutputCanvasAnchorType);
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::OutputCanvasAnchorType>(value) == ticket->getIntent()->getOutputCanvas().outputCanvasAnchor;
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasOrientation",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ContentOrientation);
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::ContentOrientation>(value) == ticket->getIntent()->getOutputCanvas().outputCanvasOrientation;
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundColorRemoval",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getBackgroundColorRemoval();
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundNoiseRemoval",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);                
                return Map2CheckerTicketMethod::getValue<bool>(value) == ticket->getIntent()->getBackgroundNoiseRemoval();
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundColorRemovalLevel",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);
                return Map2CheckerTicketMethod::getValue<int32_t>(value) == ticket->getIntent()->getBackgroundColorRemovalLevel();
            }
        },
        {
            "pipelineOptions/imageModifications/blackEnhancementLevel",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);
                return Map2CheckerTicketMethod::getValue<int32_t>(value) == ticket->getIntent()->getBlackEnhancementLevel();
            }
        },
        {
            "dest/print/mediaSize",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSizeId);         
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSizeId>(value) == ticket->getIntent()->getOutputMediaSizeId();
            }
        },
        // {
        //     TicketSettingEnum::outputMediaOrientation,                         
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaOrientation);    
        //         return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaOrientation>(value) == ticket->getIntent()->getOutputMediaOrientation();
        //     }
        // },
        {
            "dest/print/mediaType",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaIdType);         
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaIdType>(value) == ticket->getIntent()->getOutputMediaIdType();
            }
        },
        {
            "dest/print/mediaSource",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSource);
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSource>(value) == ticket->getIntent()->getOutputMediaSource();
            }
        },
        {
            "dest/print/mediaDestination",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaDestinationId);
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaDestinationId>(value) == ticket->getIntent()->getOutputDestination();
            }
        },
        {
            "dest/print/foldingStyleId",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);
                return Map2CheckerTicketMethod::getValue<int>(value) == ticket->getIntent()->getFoldingStyleId();
            }
        },
        {
            "dest/print/plexMode",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::Plex);                
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::Plex>(value) == ticket->getIntent()->getOutputPlexMode();
            }
        },
        {
            "dest/print/duplexBinding",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::PlexBinding);         
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::PlexBinding>(value) == ticket->getIntent()->getOutputPlexBinding();
            }
        },
        {
            "dest/print/copies",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);
                return Map2CheckerTicketMethod::getValue<int>(value) == ticket->getIntent()->getCopies();
            }
        },
        {
            "dest/print/collate",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::SheetCollate);
                return Map2CheckerTicketMethod::getValue<dune::copy::SheetCollate>(value) == ticket->getIntent()->getCollate();
            }
        },
        {
            "dest/print/printQuality",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::PrintQuality);
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::PrintQuality>(value) == ticket->getIntent()->getCopyQuality();
            }
        },
        // {
        //     TicketSettingEnum::resize,                                         
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);               
        //         return Map2CheckerTicketMethod::getValue<int>(value) == ticket->getIntent()->getResize();
        //     }
        // },
        // {
        //     TicketSettingEnum::lighterDarker,                                  
        //     [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
        //     { 
        //         Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);               
        //         return Map2CheckerTicketMethod::getValue<int>(value) == ticket->getIntent()->getLighterDarker();
        //     }
        // },
        {
            "dest/print/printingOrder",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::PrintingOrder);
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::PrintingOrder>(value) == ticket->getIntent()->getPrintingOrder();
            }
        },
        {
            "dest/print/mediaFamily",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaFamily);
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaFamily>(value) == ticket->getIntent()->getMediaFamily();
            }
        },
        {
            "dest/print/rotate",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::Rotate);
                dune::imaging::types::Rotate tempRotate{dune::imaging::types::Rotate::AUTO};
                if (ticket->getIntent()->getAutoRotate() == false)
                {
                    tempRotate = dune::job::cdm::mapFromCdm(dune::job::cdm::mapToCdmRotate(ticket->getIntent()->getRotation()));
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::Rotate>(value) == tempRotate;
            }
        },
        {
            "dest/print/printMargins",
            [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::CopyMargins);
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::CopyMargins>(value) == ticket->getIntent()->getCopyMargins();
            }
        }
    };
};

/**
 * @brief Namespace to encapsulate mapper checker for parser ticket table method 
 */
namespace Map2CheckerTicketTableMethod
{
    /**
     * @brief Unordered map to manage check between a CopyIntentValuesUnion with a ticket table
     * 
     * string used as key, indicate the getter to ticket
     * 
     * ? If there is any setting not covered, add here.
     * ? Maintain a few the order of first scan settings, then part of copy-print.
     * ? Take care to add enum ticket setting on fbs if you need a new one.
     */
    static std::unordered_map<std::string, std::function<bool(CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable)>> MAP
    {
        {
            "src/scan/resolution",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::Resolution);
                if(ticketTable == nullptr || ticketTable->src.get() == nullptr || ticketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP src/scan/resolution there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::Resolution>(value) == dune::job::cdm::mapFromCdm(ticketTable->src.get()->scan.get()->resolution.get());
            }
        },
        {
            "src/scan/colorMode",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ColorMode);           
                if(ticketTable == nullptr || ticketTable->src.get() == nullptr || ticketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP src/scan/colorMode there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::ColorMode>(value) == dune::job::cdm::mapFromCdm(ticketTable->src.get()->scan.get()->colorMode.get());
            }
        },
        {
            "src/scan/contentType",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            { 
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::OriginalContentType);
                if(ticketTable == nullptr || ticketTable->src.get() == nullptr || ticketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP src/scan/contentType there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::OriginalContentType>(value) == dune::job::cdm::mapFromCdm(ticketTable->src.get()->scan.get()->contentType.get());
            }
        },
        {
            "src/scan/mediaType",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::OriginalMediaType);
                if(ticketTable == nullptr || ticketTable->src.get() == nullptr || ticketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP src/scan/mediaType there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::scan::types::OriginalMediaType>(value) == dune::job::cdm::mapFromCdm(ticketTable->src.get()->scan.get()->mediaType.get());
            }
        },
        {
            "src/scan/scanAcquisitionsSpeed",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ScanAcquisitionsSpeedEnum); 
                if(ticketTable == nullptr || ticketTable->src.get() == nullptr || ticketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP src/scan/scanAcquisitionsSpeed there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::scan::types::ScanAcquisitionsSpeedEnum>(value) == dune::job::cdm::mapFromCdm(ticketTable->src.get()->scan.get()->scanAcquisitionsSpeed.get());
            }
        },
        {
            "src/scan/autoDeskew",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);
                if(ticketTable == nullptr || ticketTable->src.get() == nullptr || ticketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP src/scan/autoDeskew there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<bool>(value) == dune::job::cdm::mapFromCdm(ticketTable->src.get()->scan.get()->autoDeskew.get());
            }
        },
        {
            "src/scan/invertColors",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);
                if(ticketTable == nullptr || ticketTable->src.get() == nullptr || ticketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP src/scan/invertColors there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<bool>(value) == dune::job::cdm::mapFromCdm(ticketTable->src.get()->scan.get()->invertColors.get());
            }
        },
        {
            "src/scan/edgeToEdgeScan",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);
                if(ticketTable == nullptr || ticketTable->src.get() == nullptr || ticketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP src/scan/edgeToEdgeScan there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<bool>(value) == dune::job::cdm::mapFromCdm(ticketTable->src.get()->scan.get()->edgeToEdgeScan.get());
            }
        },
        {
            "pipelineOptions/manualUserOperations/autoRelease",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->manualUserOperations.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/manualUserOperations/autoRelease there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<bool>(value) == dune::job::cdm::mapFromCdm(ticketTable->pipelineOptions.get()->manualUserOperations.get()->autoRelease.get());
            }
        },
        {
            "pipelineOptions/scaling/scaleSelection",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ScanScaleSelectionEnum); 
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->scaling.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/scaling/scaleSelection there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::scan::types::ScanScaleSelectionEnum>(value) == dune::job::cdm::mapFromCdm(ticketTable->pipelineOptions.get()->scaling.get()->scaleSelection.get());
            }
        },
        {
            "pipelineOptions/scaling/scaleToSize",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSizeId);
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->scaling.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/scaling/scaleToSize there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSizeId>(value) == dune::job::cdm::mapFromCdm(ticketTable->pipelineOptions.get()->scaling.get()->scaleToSize.get());
            }
        },
        {
            "pipelineOptions/scaling/scaleToOutput",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSource);
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->scaling.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/scaling/scaleToOutput there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSource>(value) == dune::job::cdm::mapFromCdm(ticketTable->pipelineOptions.get()->scaling.get()->scaleToOutput.get());
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasMediaSize",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSizeId);
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/imageModifications/outputCanvasMediaSize there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSizeId>(value) == dune::job::cdm::mapFromCdm(ticketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasMediaSize.get());
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasMediaId",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSource);
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/imageModifications/outputCanvasMediaId there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSource>(value) == dune::job::cdm::mapFromCdm(ticketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasMediaId.get());
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasCustomWidth",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::DOUBLE);
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/imageModifications/outputCanvasCustomWidth there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<double>(value) == ticketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth.get();
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasCustomLength",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::DOUBLE);
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/imageModifications/outputCanvasCustomLength there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<double>(value) == ticketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomLength.get();
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasAnchor",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::OutputCanvasAnchorType);
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/imageModifications/outputCanvasAnchor there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::OutputCanvasAnchorType>(value) == dune::job::cdm::mapFromCdm(ticketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasAnchor.get());
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasOrientation",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::ContentOrientation);
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/imageModifications/outputCanvasOrientation there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::ContentOrientation>(value) == dune::job::cdm::mapFromCdm(ticketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasOrientation.get());
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundColorRemoval",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::BOOL);
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/imageModifications/backgroundColorRemoval there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<bool>(value) == dune::job::cdm::mapFromCdm(ticketTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemoval.get());
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundColorRemovalLevel",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/imageModifications/backgroundColorRemovalLevel there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<int32_t>(value) == ticketTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemovalLevel.get();
            }
        },
        {
            "pipelineOptions/imageModifications/blackEnhancementLevel",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);
                if(ticketTable == nullptr || ticketTable->pipelineOptions.get() == nullptr || ticketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP pipelineOptions/imageModifications/blackEnhancementLevel there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<int32_t>(value) == ticketTable->pipelineOptions.get()->imageModifications.get()->blackEnhancementLevel.get();
            }
        },
        {
            "dest/print/mediaSource",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSource);
                if(ticketTable == nullptr || ticketTable->dest.get() == nullptr || ticketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP dest/print/mediaSource there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSource>(value) == dune::job::cdm::mapFromCdm(ticketTable->dest.get()->print.get()->mediaSource.get());
            }
        },
        {
            "dest/print/mediaDestination",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaDestinationId);
                if(ticketTable == nullptr || ticketTable->dest.get() == nullptr || ticketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP dest/print/mediaDestination there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaDestinationId>(value) == dune::job::cdm::mapFromCdm(ticketTable->dest.get()->print.get()->mediaDestination.get());
            }
        },
        {
            "dest/print/foldingStyleId",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);
                if(ticketTable == nullptr || ticketTable->dest.get() == nullptr || ticketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP dest/print/foldingStyleId there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<int>(value) == ticketTable->dest.get()->print.get()->foldingStyleId.get();
            }
        },
        {
            "dest/print/copies",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::INT32);
                if(ticketTable == nullptr || ticketTable->dest.get() == nullptr || ticketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP dest/print/copies there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<int>(value) == ticketTable->dest.get()->print.get()->copies.get();
            }
        },
        {
            "dest/print/collate",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::SheetCollate);
                if(ticketTable == nullptr || ticketTable->dest.get() == nullptr || ticketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP dest/print/collate there is any table that not have value, return false");
                    return false;
                } 
                return Map2CheckerTicketMethod::getValue<dune::copy::SheetCollate>(value) == dune::job::cdm::mapFromCdm(ticketTable->dest.get()->print.get()->collate.get());
            }
        },
        {
            "dest/print/printQuality",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::PrintQuality);
                if(ticketTable == nullptr || ticketTable->dest.get() == nullptr || ticketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP dest/print/printQuality there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::PrintQuality>(value) == dune::job::cdm::mapFromCdm(ticketTable->dest.get()->print.get()->printQuality.get());
            }
        },
        {
            "dest/print/printingOrder",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::PrintingOrder);
                if(ticketTable == nullptr || ticketTable->dest.get() == nullptr || ticketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP dest/print/printingOrder there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::PrintingOrder>(value) == dune::job::cdm::mapFromCdm(ticketTable->dest.get()->print.get()->printingOrder.get());
            }
        },
        {
            "dest/print/mediaFamily",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaFamily);
                if(ticketTable == nullptr || ticketTable->dest.get() == nullptr || ticketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP dest/print/mediaFamily there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaFamily>(value) == dune::job::cdm::mapFromCdm(ticketTable->dest.get()->print.get()->mediaFamily.get());
            }
        },
        {
            "dest/print/rotate",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::Rotate);
                if(ticketTable == nullptr || ticketTable->dest.get() == nullptr || ticketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP dest/print/rotate there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::Rotate>(value) == dune::job::cdm::mapFromCdm(ticketTable->dest.get()->print.get()->rotate.get());
            }
        },
        {
            "dest/print/printMargins",              
            [](CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable) -> bool 
            {
                Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::CopyMargins);
                if(ticketTable == nullptr || ticketTable->dest.get() == nullptr || ticketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerTicketTableMethod::MAP dest/print/printMargins there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerTicketMethod::getValue<dune::imaging::types::CopyMargins>(value) == dune::job::cdm::mapFromCdm(ticketTable->dest.get()->print.get()->printMargins.get());
            }
        }
    };
};

namespace Map2CheckerCdmTableProperty
{
    /**
     * @brief Check property method for enums     
     * @tparam CdmClass enum type on cdm layer
     * @param property optional property from table
     * @param settingIsSetOnCdm boolean reference to notify client if setting is currently set
     * @param currentConstraints constraints to check if current value need to be changed
     * @return true if property need to be changed
     * @return false if no
     */
    template<typename CdmClass>
    inline bool checkPropertyEnum(dune::cdm::easyBuffers::OptionalProperty<CdmClass> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty Going to check property on table");
        bool result = false;
        if (property.isSet(dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH))
        {
            auto cdmVal = property.get();
            
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty table is set, going to check value");
            
            if(dune::job::cdm::hasValue<decltype(cdmVal)>(cdmVal))
            {
                settingIsSetOnCdm = true;

                CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty value is not undefined");
                if( currentConstraints != nullptr && !currentConstraints->tryValidate(&cdmVal))
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::checkProperty Founded and not pass constraints");
                    result = true;
                }
            }
        }
        return result;
    }

    // ? Add any type not currently supported
    /**
     * @brief Check property method template to check if a value is set and valid on constraints
     * @param property optional property from table
     * @param settingIsSetOnCdm boolean reference to notify client if setting is currently set
     * @param currentConstraints constraints to check if current value need to be changed
     * @return true if property need to be changed
     * @return false if no
     */

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::CollateModes> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::CollateModes>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::ColorModes> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::ColorModes>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::Resolutions> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::Resolutions>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::AutoColorDetect> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::AutoColorDetect>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::CcdChannel> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::CcdChannel>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::BinaryRendering> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::BinaryRendering>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::ScanCaptureMode> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::ScanCaptureMode>(property,settingIsSetOnCdm,currentConstraints);
    }
    
    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::ContentType> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::ContentType>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::PagesPerSheet> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::PagesPerSheet>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::ScanAcquisitionsSpeed> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::ScanAcquisitionsSpeed>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::PrintingOrder> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::PrintingOrder>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::PrintMargins> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::PrintMargins>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::OutputCanvasAnchor> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::OutputCanvasAnchor>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::ContentOrientation> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::glossary_1::ContentOrientation>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::DuplexBinding> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::glossary_1::DuplexBinding>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::MediaDestinationId> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::glossary_1::MediaDestinationId>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::MediaSize> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::glossary_1::MediaSize>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::MediaSourceId> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::glossary_1::MediaSourceId>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::MediaType> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::glossary_1::MediaType>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::PlexMode> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::glossary_1::PlexMode>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::PrintQuality> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::glossary_1::PrintQuality>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::ScanMediaSourceId> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::glossary_1::ScanMediaSourceId>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::ScanMediaType> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::glossary_1::ScanMediaType>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::scaling::ScaleSelection> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        return checkPropertyEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::FeatureEnabled> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {
        return checkPropertyEnum<dune::cdm::glossary_1::FeatureEnabled>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::FeatureEnabledEnum> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty Going to check property on table");
        bool result = false;
        if (property.isSet(dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH))
        {
            auto cdmVal = property.get();
            
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty table is set, going to check value");
            
            if(dune::job::cdm::hasValue<dune::cdm::glossary_1::FeatureEnabled>(cdmVal))
            {
                settingIsSetOnCdm = true;

                CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty value is not undefined");
                if( currentConstraints != nullptr && !currentConstraints->tryValidate(&cdmVal))
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::checkProperty Founded and not pass constraints");
                    result = true;
                }
            }
        }
        return result;
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::Rotate> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {
        return checkPropertyEnum<dune::cdm::jobTicket_1::Rotate>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::RotateEnum> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty Going to check property on table");
        bool result = false;
        if (property.isSet(dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH))
        {
            auto cdmVal = property.get();
            
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty table is set, going to check value");
            
            if(dune::job::cdm::hasValue<dune::cdm::jobTicket_1::Rotate>(cdmVal))
            {
                settingIsSetOnCdm = true;

                CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty value is not undefined");
                if( currentConstraints != nullptr && !currentConstraints->tryValidate(&cdmVal))
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::checkProperty Founded and not pass constraints");
                    result = true;
                }
            }
        }
        return result;
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::MediaOrientationEnum> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty Going to check property on table");
        bool result = false;
        if (property.isSet(dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH))
        {
            auto cdmVal = property.get();
            
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty table is set, going to check value");
            
            if(dune::job::cdm::hasValue<dune::cdm::glossary_1::MediaOrientation>(cdmVal))
            {
                settingIsSetOnCdm = true;

                CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty value is not undefined");
                if( currentConstraints != nullptr && !currentConstraints->tryValidate(&cdmVal))
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::checkProperty Founded and not pass constraints");
                    result = true;
                }
            }
        }
        return result;
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<dune::cdm::mediaProfile_1::MediaFamilyEnum> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {   
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty Going to check property on table");
        bool result = false;
        if (property.isSet(dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH))
        {
            auto cdmVal = property.get();
            
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty table is set, going to check value");
            
            if(dune::job::cdm::hasValue<dune::cdm::mediaProfile_1::MediaFamily>(cdmVal))
            {
                settingIsSetOnCdm = true;

                CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty value is not undefined");
                if( currentConstraints != nullptr && !currentConstraints->tryValidate(&cdmVal))
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::checkProperty Founded and not pass constraints");
                    result = true;
                }
            }
        }
        return result;
    }

    /**
     * @brief Check property method for int32
     * @param property optional property from table
     * @param settingIsSetOnCdm boolean reference to notify client if setting is currently set
     * @param currentConstraints constraints to check if current value need to be changed
     * @return true if property need to be changed
     * @return false if no
     */
    template<typename primitiveType>
    inline bool checkPropertyFundamentalType(dune::cdm::easyBuffers::OptionalProperty<primitiveType> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty Going to check property on table");
        bool result = false;
        if (property.isSet(dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH))
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCdmTableProperty::checkProperty table is set, going to check value");                    
            auto cdmVal = property.get();
            settingIsSetOnCdm = true;

            if( currentConstraints != nullptr && !currentConstraints->tryValidate(&cdmVal))
            {
                CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::checkProperty Founded and not pass constraints");
                result = true;
            }

        }
        return result;
    }


    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<int32_t> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {
        return checkPropertyFundamentalType<int32_t>(property,settingIsSetOnCdm,currentConstraints);
    }

    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<uint32_t> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {
        return checkPropertyFundamentalType<uint32_t>(property,settingIsSetOnCdm,currentConstraints);
    }
    inline bool checkProperty(dune::cdm::easyBuffers::OptionalProperty<double> property, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {
        return checkPropertyFundamentalType<double>(property,settingIsSetOnCdm,currentConstraints);
    }

    // ? Could be settings that are not supported on future, add any new if its needed for constraint auto adjust reach the case on future
    static std::unordered_map<std::string,
            std::function<bool(const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, 
                                bool& settingIsSetOnCdm, 
                                std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)>
            > MAP
    {
        {
            "src/scan/colorMode",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/colorMode there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->colorMode,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/mediaSource",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/mediaSource there is any table that not have value, return false");
                    return false;
                }                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->mediaSource,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/mediaSize",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/mediaSize there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->mediaSize,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/xOffset",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/xOffset there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->xOffset,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/yOffset",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/yOffset there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->yOffset,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/plexMode",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/plexMode there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->plexMode,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/resolution",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/resolution there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->resolution,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/pageBinding",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/pageBinding there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->pageBinding,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/contentType",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/contentType there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->contentType,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/contentOrientation",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/contentOrientation there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->contentOrientation,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/pagesFlipUpEnabled",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/pagesFlipUpEnabled there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->pagesFlipUpEnabled,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/autoColorDetect",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            {
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/autoColorDetect there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->autoColorDetect,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/blackBackground",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/blackBackground there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->blackBackground,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/mediaType",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/mediaType there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->mediaType,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/autoExposure",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/autoExposure there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->autoExposure,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/gamma",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/gamma there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->gamma,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/highlight",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/highlight there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->highlight,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/colorSensitivity",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/colorSensitivity there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->colorSensitivity,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/colorRange",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/colorRange there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->colorRange,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/ccdChannel",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/ccdChannel there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->ccdChannel,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/binaryRendering",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/binaryRendering there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->binaryRendering,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/descreen",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/descreen there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->descreen,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/feederPickStop",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/feederPickStop there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->feederPickStop,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/shadow",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/shadow there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->shadow,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/compressionFactor",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/compressionFactor there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->compressionFactor,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/threshold",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/threshold there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->threshold,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/scanCaptureMode",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/scanCaptureMode there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->scanCaptureMode,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/scanAcquisitionsSpeed",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/scanAcquisitionsSpeed there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->scanAcquisitionsSpeed,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/autoDeskew",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/autoDeskew there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->autoDeskew,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/edgeToEdgeScan",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/edgeToEdgeScan there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->edgeToEdgeScan,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/longPlotScan",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/longPlotScan there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->longPlotScan,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "src/scan/invertColors",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/invertColors there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->invertColors,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/sharpness",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/invertColors there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->sharpness,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundCleanup",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/backgroundCleanup there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->backgroundCleanup,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/exposure",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/exposure there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->exposure,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/contrast",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/contrast there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->contrast,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/blankPageSuppressionEnabled",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/blankPageSuppressionEnabled there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->blankPageSuppressionEnabled,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/pagesPerSheet",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/pagesPerSheet there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->pagesPerSheet,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasMediaSize",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/outputCanvasMediaSize there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasMediaSize,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasMediaId",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/outputCanvasMediaId there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasMediaId,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasCustomWidth",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/outputCanvasCustomWidth there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasCustomLength",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/outputCanvasCustomLength there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomLength,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasAnchor",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/outputCanvasAnchor there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasAnchor,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasOrientation",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/outputCanvasOrientation there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasOrientation,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundNoiseRemoval",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/backgroundNoiseRemoval there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->backgroundNoiseRemoval,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundColorRemoval",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/backgroundColorRemoval there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemoval,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundColorRemovalLevel",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/backgroundColorRemovalLevel there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemovalLevel,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/blackEnhancementLevel",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/imageModifications/blackEnhancementLevel there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->blackEnhancementLevel,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/manualUserOperations/imagePreviewConfiguration",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->manualUserOperations.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/manualUserOperations/imagePreviewConfiguration there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->manualUserOperations.get()->imagePreviewConfiguration,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/manualUserOperations/autoRelease",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->manualUserOperations.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/manualUserOperations/autoRelease there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->manualUserOperations.get()->autoRelease,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/scaling/scaleToFitEnabled",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->scaling.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/scaling/scaleToFitEnabled there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->scaling.get()->scaleToFitEnabled,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/scaling/xScalePercent",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->scaling.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/scaling/xScalePercent there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->scaling.get()->xScalePercent,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/scaling/yScalePercent",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->scaling.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/scaling/yScalePercent there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->scaling.get()->yScalePercent,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/scaling/scaleSelection",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->scaling.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/scaling/scaleSelection there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->scaling.get()->scaleSelection,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/scaling/scaleToOutput",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->scaling.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/scaling/scaleToOutput there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->scaling.get()->scaleToOutput,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "pipelineOptions/scaling/scaleToSize",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->pipelineOptions.get() == nullptr || updatedJobTicketTable->pipelineOptions.get()->scaling.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipelineOptions/scaling/scaleToSize there is any table that not have value, return false");
                    return false;
                }
               return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->pipelineOptions.get()->scaling.get()->scaleToSize,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/collate",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/collate there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->collate,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/colorMode",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/colorMode there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->colorMode,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/copies",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/copies there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->copies,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/mediaSource",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/mediaSource there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->mediaSource,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/mediaDestination",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/mediaDestination there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->mediaDestination,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/foldingStyleId",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/foldingStyleId there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->foldingStyleId,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/mediaSize",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/mediaSize there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->mediaSize,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/mediaType",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/mediaType there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->mediaType,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/foldingStyleId",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/foldingStyleId there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->foldingStyleId,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/plexMode",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/plexMode there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->plexMode,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/duplexBinding",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/duplexBinding there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->duplexBinding,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/printQuality",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/printQuality there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->printQuality,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/resolution",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/resolution there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->resolution,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/printingOrder",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/printingOrder there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->printingOrder,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/mediaFamily",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/mediaFamily there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->mediaFamily,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/rotate",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/rotate there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->rotate,settingIsSetOnCdm,currentConstraints);
            }
        },
        {
            "dest/print/printMargins",
            [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                if(updatedJobTicketTable == nullptr || updatedJobTicketTable->dest.get() == nullptr || updatedJobTicketTable->dest.get()->print.get() == nullptr)
                {
                    CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest/print/printMargins there is any table that not have value, return false");
                    return false;
                }
                return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->dest.get()->print.get()->printMargins,settingIsSetOnCdm,currentConstraints);
            }
        }
    };

    inline bool executeMapFunction(const std::string &cdmSettingString,
                                const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, 
                                bool& settingIsSetOnCdm, 
                                std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints = std::shared_ptr<dune::framework::data::constraints::Constraints>(nullptr))
    {
        auto pair = Map2CheckerCdmTableProperty::MAP.find(cdmSettingString);
        assert_msg(pair != Map2CheckerCdmTableProperty::MAP.end(),"Unsupported setting %s on scan table expected, return as error", cdmSettingString.c_str());
        return pair->second(updatedJobTicketTable, settingIsSetOnCdm, currentConstraints);
    }
};

namespace Map2CheckerCopyJobTicketProperty
{

    template<typename CdmType>
    inline bool checkType(CdmType cdmVal,std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCopyJobTicketProperty::checkType checking constraint on job ticket enter");
        bool result = false;

        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCopyJobTicketProperty::checkType checking constraint get ok");
        // If have constraints and when try to validate, value is not accepted, then result os true
        if( currentConstraints != nullptr && !currentConstraints->tryValidate(&cdmVal))
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCopyJobTicketProperty::checkType checking constraint get result true");
            result = true;
        }

        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2CheckerCopyJobTicketProperty::checkType checking constraint exit");
        return result;
    }

    // ? Could be settings that are not supported on future, add any new if its needed for constraint auto adjust reach the case on future
    static std::unordered_map<std::string, std::function<bool(std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)>> MAP
    {
        {
            "src/scan/colorMode",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getColorMode()),currentConstraints);
            }
        },
        {
            "src/scan/mediaSource",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getScanSource()),currentConstraints);
            }
        },
        {
            "src/scan/mediaSize",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getInputMediaSizeId()),currentConstraints);
            }
        },
        {
            "src/scan/xOffset",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getXOffset(),currentConstraints);
            }
        },
        {
            "src/scan/yOffset",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getYOffset(),currentConstraints);
            }
        },
        {
            "src/scan/plexMode",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getInputPlexMode()),currentConstraints);
            }
        },
        {
            "src/scan/resolution",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getOutputXResolution()),currentConstraints);
            }
        },
        // Not supported at ticket level
        // {
        //     "src/scan/pageBinding",
        //     [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
        //     { 
        //         return checkType(ticket->getIntent()->getPageBinding(),currentConstraints);
        //     }
        // },
        {
            "src/scan/contentType",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getOriginalContentType()),currentConstraints);
            }
        },
        {
            "src/scan/contentOrientation",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getContentOrientation()),currentConstraints);
            }
        },
        {
            "src/scan/pagesFlipUpEnabled",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getScanPagesFlipUpEnabled()),currentConstraints);
            }
        },
        {
            "src/scan/autoColorDetect",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getScanAutoColorDetect()),currentConstraints);
            }
        },
        {
            "src/scan/blackBackground",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getScanBlackBackground()),currentConstraints);
            }
        },
        {
            "src/scan/mediaType",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getOriginalMediaType()),currentConstraints);
            }
        },
        {
            "src/scan/autoExposure",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getScanAutoExposure()),currentConstraints);
            }
        },
        {
            "src/scan/gamma",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getScanGamma(),currentConstraints);
            }
        },
        {
            "src/scan/highlight",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getScanHighlight(),currentConstraints);
            }
        },
        {
            "src/scan/colorSensitivity",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getScanColorSensitivity(),currentConstraints);
            }
        },
        {
            "src/scan/colorRange",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getScanColorRange(),currentConstraints);
            }
        },
        {
            "src/scan/ccdChannel",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getCcdChannel()),currentConstraints);
            }
        },
        {
            "src/scan/binaryRendering",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getBinaryRendering()),currentConstraints);
            }
        },
        {
            "src/scan/descreen",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getDescreen()),currentConstraints);
            }
        },
        {
            "src/scan/feederPickStop",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getFeederPickStop()),currentConstraints);
            }
        },
        {
            "src/scan/shadow",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getShadow(),currentConstraints);
            }
        },
        {
            "src/scan/compressionFactor",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getCompressionFactor(),currentConstraints);
            }
        },
        {
            "src/scan/threshold",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getThreshold(),currentConstraints);
            }
        },
        {
            "src/scan/scanCaptureMode",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getScanCaptureMode()),currentConstraints);
            }
        },
        {
            "src/scan/scanAcquisitionsSpeed",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getScanAcquisitionsSpeed()),currentConstraints);
            }
        },
        {
            "src/scan/autoDeskew",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getAutoDeskew()),currentConstraints);
            }
        },
        {
            "src/scan/edgeToEdgeScan",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getEdgeToEdgeScan()),currentConstraints);
            }
        },
        {
            "src/scan/longPlotScan",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getLongPlotScan()),currentConstraints);
            }
        },
        {
            "src/scan/invertColors",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getInvertColors()),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/sharpness",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getSharpen(),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundCleanup",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getBackgroundRemoval(),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/exposure",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getBrightness(),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/contrast",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getContrast(),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/blankPageSuppressionEnabled",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getBlankPageDetection() == dune::scan::types::BlankDetectEnum::DetectAndSupress),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/pagesPerSheet",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getPagesPerSheet()),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasMediaSize",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getOutputCanvas().outputCanvasMediaSize),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasMediaId",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getOutputCanvas().outputCanvasMediaId),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasCustomWidth",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                // Custom width in intents should be always ok.
                // Constraint value related with custom width from intent size is not supported
                return false;
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasCustomLength",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                // Custom Length in intents should be always ok.
                // Constraint value related with custom length from intent size is not supported
                return false;
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasAnchor",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getOutputCanvas().outputCanvasAnchor),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasOrientation",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getOutputCanvas().outputCanvasOrientation),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundNoiseRemoval",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getBackgroundNoiseRemoval()),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundColorRemoval",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getBackgroundColorRemoval()),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundColorRemovalLevel",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getBackgroundColorRemovalLevel(),currentConstraints);
            }
        },
        {
            "pipelineOptions/imageModifications/blackEnhancementLevel",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getBlackEnhancementLevel(),currentConstraints);
            }
        },
        {
            "pipelineOptions/manualUserOperations/imagePreviewConfiguration",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getImagePreview()),currentConstraints);
            }
        },
        {
            "pipelineOptions/manualUserOperations/autoRelease",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getAutoRelease()),currentConstraints);
            }
        },
        {
            "pipelineOptions/scaling/scaleToFitEnabled",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdmFeatureEnabled(ticket->getIntent()->getScaleToFitEnabled()),currentConstraints);
            }
        },
        {
            "pipelineOptions/scaling/xScalePercent",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getXScalePercent(),currentConstraints);
            }
        },
        {
            "pipelineOptions/scaling/yScalePercent",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getYScalePercent(),currentConstraints);
            }
        },
        {
            "pipelineOptions/scaling/scaleSelection",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getScaleSelection()),currentConstraints);
            }
        },
        {
            "pipelineOptions/scaling/scaleToOutput",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getScaleToOutput()),currentConstraints);
            }
        },
        {
            "pipelineOptions/scaling/scaleToSize",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getScaleToSize()),currentConstraints);
            }
        },
        {
            "dest/print/collate",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getCollate()),currentConstraints);
            }
        },
        // Unsupported for the moment, applied from scan part
        // {
        //     "dest/print/colorMode",
        //     [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
        //     { 
        //         return false;
        //     }
        // },
        {
            "dest/print/copies",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getCopies(),currentConstraints);
            }
        },
        {
            "dest/print/mediaSource",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getOutputMediaSource()),currentConstraints);
            }
        },
        {
            "dest/print/mediaDestination",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getOutputDestination()),currentConstraints);
            }
        },
        {
            "dest/print/foldingStyleId",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(ticket->getIntent()->getFoldingStyleId(),currentConstraints);
            }
        },
        {
            "dest/print/mediaSize",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
                return checkType(mediaCdmHelper.convertDuneMediaIdSizeToCdm(ticket->getIntent()->getOutputMediaSizeId()),currentConstraints);
            }
        },
        {
            "dest/print/mediaType",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getOutputMediaIdType()),currentConstraints);
            }
        },
        {
            "dest/print/plexMode",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getOutputPlexMode()),currentConstraints);
            }
        },
        {
            "dest/print/duplexBinding",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getOutputPlexBinding()),currentConstraints);
            }
        },
        {
            "dest/print/printQuality",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getCopyQuality()),currentConstraints);
            }
        },
        // Not supported, expected on scan part
        // {
        //     "dest/print/resolution",
        //     [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
        //     { 
        //         return false;
        //     }
        // },
        {
            "dest/print/printingOrder",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getPrintingOrder()),currentConstraints);
            }
        },
        {
            "dest/print/mediaFamily",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getMediaFamily()),currentConstraints);
            }
        },
        {
            "dest/print/rotate",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                dune::imaging::types::Rotate tempRotate{dune::imaging::types::Rotate::AUTO};
                if (ticket->getIntent()->getAutoRotate() == false)
                {
                    tempRotate = dune::job::cdm::mapFromCdm(dune::job::cdm::mapToCdmRotate(ticket->getIntent()->getRotation())); 
                }
                return checkType(dune::job::cdm::mapToCdm(tempRotate), currentConstraints);
            }
        },
        {
            "dest/print/printMargins",
            [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getCopyMargins()),currentConstraints);
            }
        }
    };

    inline bool executeMapFunction(const std::string &cdmSettingString,
                                std::shared_ptr<ICopyJobTicket> ticket,
                                std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {
        auto pair = Map2CheckerCopyJobTicketProperty::MAP.find(cdmSettingString);
        assert_msg(pair != Map2CheckerCopyJobTicketProperty::MAP.end(),"Unsupported setting %s on job ticket map expected, return as error", cdmSettingString.c_str());
        return pair->second(ticket, currentConstraints);
    }
};

namespace Map2UpdateTableProperty
{
    template<typename CdmType>
    inline void getFirstValueFromConstraintsEnum(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints,CdmType& cdmValue)
    {
        // Take previous valid values
        for(auto constraint : currentConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
            {
                cdmValue = (static_cast< dune::framework::data::constraints::ValidValuesEnum<CdmType>*>(constraint))->getValidValues()[0];
                break;
            }
        }
    }

    inline void getFirstValueFromConstraintsValidBool(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints,bool& cdmValue)
    {
        // Take previous valid values
        for(auto constraint : currentConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_BOOL)
            {
                cdmValue = (static_cast< dune::framework::data::constraints::ValidValuesBool*>(constraint))->getValidValues()[0];
                break;
            }
        }
    }
    template<typename CdmType>
    inline void getFirstValueFromConstraintsValidShort(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, CdmType& cdmValue)
    {
        // Take previous valid values
        for(auto constraint : currentConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_SHORT)
            {
                cdmValue = (static_cast< dune::framework::data::constraints::ValidValuesShort*>(constraint))->getValidValues()[0];
                break;
            }
        }
    }

    inline void getFirstValueFromConstraintsValidString(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints,std::string& cdmValue)
    {
        // Take previous valid values
        for(auto constraint : currentConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_STRING)
            {
                cdmValue = (static_cast< dune::framework::data::constraints::ValidValuesString*>(constraint))->getValidValues()[0];
                break;
            }
        }
    }

    inline void getFirstValueFromConstraintsMinLength(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints,size_t& cdmValue)
    {
        // Take previous valid values
        for(auto constraint : currentConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::MIN_LENGTH)
            {
                cdmValue = (static_cast< dune::framework::data::constraints::MinLength*>(constraint))->getMinLength();
                break;
            }
        }
    }

    inline void getFirstValueFromConstraintsMaxLength(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints,size_t& cdmValue)
    {
        // Take previous valid values
        for(auto constraint : currentConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::MAX_LENGTH)
            {
                cdmValue = (static_cast< dune::framework::data::constraints::MaxLength*>(constraint))->getMaxLength();
                break;
            }
        }
    }

    // inline void getFirstValueFromConstraintsMinCount(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints,size_t& cdmValue)
    // {
    //     // Take previous valid values
    //     for(auto constraint : currentConstraints->getConstraints())
    //     {
    //         if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::MIN_COUNT)
    //         {
    //             cdmValue = (static_cast< dune::framework::data::constraints::MinCount*>(constraint))->getMinCount();
    //             break;    
    //         }
    //     }
    // }

    // inline void getFirstValueFromConstraintsMaxCount(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints,size_t& cdmValue)
    // {
    //     // Take previous valid values
    //     for(auto constraint : currentConstraints->getConstraints())
    //     {
    //         if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::MAX_COUNT)
    //         {
    //             cdmValue = (static_cast< dune::framework::data::constraints::MaxCount*>(constraint))->getMaxCount();
    //             break;    
    //         }
    //     }
    // }

    inline void getNearestValueFromConstraintsRange(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, int32_t& cdmValue)
    {
        // Take previous valid values
        for(auto constraint : currentConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::RANGE_INT)
            {
                // Take nearest value as default expected
                auto rangeIntConstraint = (static_cast< dune::framework::data::constraints::RangeInt*>(constraint));
                if (cdmValue < rangeIntConstraint->getMin())
                {
                    cdmValue = rangeIntConstraint->getMin();
                }
                else if (cdmValue > rangeIntConstraint->getMax())
                {
                    cdmValue = rangeIntConstraint->getMax();
                }
                else if(rangeIntConstraint->getStep() > 1)
                {
                    auto differValue = (cdmValue - rangeIntConstraint->getMin()) % rangeIntConstraint->getStep();
                    cdmValue = cdmValue - differValue;
                }
                else // take middle value when step is zero, normally this range will not be reach because of the constraint
                {
                    cdmValue = (int)(rangeIntConstraint->getMax() + std::abs(rangeIntConstraint->getMin()))/(int)2;
                }
                break;
            }
        }
    }

    inline void getNearestValueFromConstraintsRange(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, uint32_t& cdmValue)
    {
        // In general this path is not expected because constraint can only works with INT.
        // But exist to cover possibility error related
        auto valueAsInt = (int)cdmValue;
        Map2UpdateTableProperty::getNearestValueFromConstraintsRange(currentConstraints,valueAsInt);
        cdmValue = (uint32_t)valueAsInt;
    }

    inline void getNearestValueFromConstraintsRange(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints,double& cdmValue)
    {
        // Take previous valid values
        for(auto constraint : currentConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::RANGE_DOUBLE)
            {
                // Take nearest value as default expected
                auto rangeDoubleConstraint = (static_cast< dune::framework::data::constraints::RangeDouble*>(constraint));
                if (cdmValue < rangeDoubleConstraint->getMin())
                {
                    cdmValue = rangeDoubleConstraint->getMin();
                }
                else if (cdmValue > rangeDoubleConstraint->getMax())
                {
                    cdmValue = rangeDoubleConstraint->getMax();
                }
                else if(rangeDoubleConstraint->getStep() > (double)0.0)
                {
                    auto differValue = std::fmod(cdmValue - rangeDoubleConstraint->getMin(), rangeDoubleConstraint->getStep());
                    cdmValue = cdmValue - differValue;
                }
                else // take middle value when step is zero, normally this range will not be reach because of the constraint
                {
                    cdmValue = (int)(rangeDoubleConstraint->getMax() + std::abs(rangeDoubleConstraint->getMin()))/(int)2;
                }
                break;
            }
        }
    }

    template<typename CdmType>
    inline bool setFirstValueOnPropertyEnum(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, dune::cdm::easyBuffers::OptionalProperty<CdmType>& property)
    {
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnPropertyEnum update constraint value enter");
        CdmType cdmValue = CdmType::_undefined_;
        Map2UpdateTableProperty::getFirstValueFromConstraintsEnum<CdmType>(currentConstraints,cdmValue);
        bool result = false;
        if(dune::job::cdm::hasValue<decltype(cdmValue)>(cdmValue))
        {                    
            property = cdmValue;
            result = true;
        }
        else
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnPropertyEnum error set on first value of property");
        }
        
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnPropertyEnum update constraint value exit");
        return result;
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::CollateModes>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::CollateModes>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::ColorModes>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::ColorModes>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::Resolutions>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::Resolutions>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::AutoColorDetect>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::AutoColorDetect>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::CcdChannel>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::CcdChannel>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::BinaryRendering>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::BinaryRendering>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::ScanCaptureMode>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::ScanCaptureMode>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::ContentType>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::ContentType>(currentConstraints,property);
    }
    
    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::PagesPerSheet>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::PagesPerSheet>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::ScanAcquisitionsSpeed>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::ScanAcquisitionsSpeed>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::PrintingOrder>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::PrintingOrder>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::mediaProfile_1::MediaFamilyEnum>& property)
    {   
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnProperty update constraint value MediaFamily enter");
        dune::cdm::mediaProfile_1::MediaFamily cdmValue = dune::cdm::mediaProfile_1::MediaFamily::_undefined_;
        Map2UpdateTableProperty::getFirstValueFromConstraintsEnum<dune::cdm::mediaProfile_1::MediaFamily>(currentConstraints,cdmValue);
        bool result = false;
        if(dune::job::cdm::hasValue<dune::cdm::mediaProfile_1::MediaFamily>(cdmValue))
        {                    
            property = cdmValue;
            result = true;
        }
        else
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnProperty error set on MediaFamily");
        }
        
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnProperty update constraint value MediaFamily exit");
        return result;
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::Rotate>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::Rotate>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::RotateEnum>& property)
    {   
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnProperty update constraint value RotateEnum enter");
        dune::cdm::jobTicket_1::Rotate cdmValue = dune::cdm::jobTicket_1::Rotate::_undefined_;
        Map2UpdateTableProperty::getFirstValueFromConstraintsEnum<dune::cdm::jobTicket_1::Rotate>(currentConstraints,cdmValue);
        bool result = false;
        if(dune::job::cdm::hasValue<dune::cdm::jobTicket_1::Rotate>(cdmValue))
        {                    
            property = cdmValue;
            result = true;
        }
        else
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnProperty error set on RotateEnum");
        }
        
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnProperty update constraint value RotateEnum exit");
        return result;
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::PrintMargins>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::PrintMargins>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::OutputCanvasAnchor>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::OutputCanvasAnchor>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::ContentOrientation>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::glossary_1::ContentOrientation>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::DuplexBinding>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::glossary_1::DuplexBinding>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::MediaDestinationId>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::glossary_1::MediaDestinationId>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::MediaSize>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::glossary_1::MediaSize>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::MediaSourceId>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::glossary_1::MediaSourceId>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::MediaType>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::glossary_1::MediaType>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::PlexMode>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::glossary_1::PlexMode>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::PrintQuality>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::glossary_1::PrintQuality>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::ScanMediaSourceId>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::glossary_1::ScanMediaSourceId>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::ScanMediaType>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::glossary_1::ScanMediaType>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::jobTicket_1::scaling::ScaleSelection>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>(currentConstraints,property);
    }

     inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::FeatureEnabled>& property)
    {   
        return setFirstValueOnPropertyEnum<dune::cdm::glossary_1::FeatureEnabled>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::FeatureEnabledEnum>& property)
    {   
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnProperty update constraint FeatureEnabled enter");
        dune::cdm::glossary_1::FeatureEnabled cdmValue = dune::cdm::glossary_1::FeatureEnabled::_undefined_;
        Map2UpdateTableProperty::getFirstValueFromConstraintsEnum<dune::cdm::glossary_1::FeatureEnabled>(currentConstraints,cdmValue);
        bool result = false;
        if(dune::job::cdm::hasValue<dune::cdm::glossary_1::FeatureEnabled>(cdmValue))
        {                    
            property = cdmValue;
            result = true;
        }
        else
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnProperty error setting FeatureEnabled value");
        }
        
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnProperty updated constraint FeatureEnabled value exit");
        return result;
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<dune::cdm::glossary_1::MediaOrientationEnum>& property)
    {   
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnProperty update constraint value MediaOrientation enter");
        dune::cdm::glossary_1::MediaOrientation cdmValue = dune::cdm::glossary_1::MediaOrientation::_undefined_;
        Map2UpdateTableProperty::getFirstValueFromConstraintsEnum<dune::cdm::glossary_1::MediaOrientation>(currentConstraints,cdmValue);
        bool result = false;
        if(dune::job::cdm::hasValue<dune::cdm::glossary_1::MediaOrientation>(cdmValue))
        {                    
            property = cdmValue;
            result = true;
        }
        else
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnProperty error set on MediaOrientation");
        }
        
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnProperty update constraint value MediaOrientation exit");
        return result;
    }

    template<typename NumberType>
    inline bool setFirstValueOnPropertyNumberType(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, dune::cdm::easyBuffers::OptionalProperty<NumberType>& property)
    {
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnPropertyNumberType update constraint value enter");
        NumberType cdmValue {0};

        bool numTypeAsEnum {false};
        bool numTypeAsShort {false};

        // Check if is possible / valid based on number check
        for(auto constraint : currentConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
            {
                numTypeAsEnum = true;
                break;
            }
            else if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_SHORT)
            {
                numTypeAsShort = true;
                break;
            }
        }

        if(numTypeAsEnum)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnPropertyNumberType type is an enum");
            Map2UpdateTableProperty::getFirstValueFromConstraintsEnum<NumberType>(currentConstraints, cdmValue);
        }
        else if (numTypeAsShort)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnPropertyNumberType type is a short");
            Map2UpdateTableProperty::getFirstValueFromConstraintsValidShort(currentConstraints, cdmValue);
        }
        else
        {
            // Copy original value to decide if is possible to set nearest value
            cdmValue = property;
            Map2UpdateTableProperty::getNearestValueFromConstraintsRange(currentConstraints, cdmValue);
        }

        property = cdmValue;        
        CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug("Map2UpdateTableProperty::setFirstValueOnPropertyNumberType update constraint value exit");
        return true;
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<int32_t>& property)
    {   
        return setFirstValueOnPropertyNumberType<int32_t>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<uint32_t>& property)
    {   
        return setFirstValueOnPropertyNumberType<uint32_t>(currentConstraints,property);
    }

    inline bool setFirstValueOnProperty(std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints, 
                                        dune::cdm::easyBuffers::OptionalProperty<double>& property)
    {   
        return setFirstValueOnPropertyNumberType<double>(currentConstraints,property);
    }

    inline void checkScanTableMutables(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable)
    {
        assert_msg(updatedJobTicketTable,"job ticket table is null, this can never occurs");
        if(updatedJobTicketTable->src.getMutable() == nullptr)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src property object is null, is need to create a new here");
            updatedJobTicketTable->src = *(std::make_unique<dune::cdm::jobTicket_1::jobTicket::SrcTable>());
            updatedJobTicketTable->src.beginMergePatch();
        }
        assert_msg(updatedJobTicketTable->src.getMutable(),"job ticket src pipeline options still be null, this can never occurs");
        if(updatedJobTicketTable->src.getMutable()->scan.getMutable() == nullptr)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP scan property object is null, is need to create a new here");
            updatedJobTicketTable->src.getMutable()->scan = *(std::make_unique<dune::cdm::jobTicket_1::ScanTable>());
            updatedJobTicketTable->src.getMutable()->scan.beginMergePatch();
        }
        assert_msg(updatedJobTicketTable->src.getMutable()->scan.getMutable(),"job ticket scan pipeline options still be null, this can never occurs");
    }

    inline void checkImageModificationsTableMutables(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable)
    {
        assert_msg(updatedJobTicketTable,"job ticket table is null, this can never occurs");
        if(updatedJobTicketTable->pipelineOptions.getMutable() == nullptr)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipeline options property object is null, is need to create a new here");
            updatedJobTicketTable->pipelineOptions = *(std::make_unique<dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable>());
            updatedJobTicketTable->pipelineOptions.getMutable()->beginMergePatch();
        }
        assert_msg(updatedJobTicketTable->pipelineOptions.getMutable(),"job ticket table pipeline options still be null, this can never occurs");
        if(updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable() == nullptr)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP manual user operations property object is null, is need to create a new here");            
            updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications = *(std::make_unique<dune::cdm::jobTicket_1::ImageModificationsTable>());
            updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.beginMergePatch();
        }
        assert_msg(updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable(),"job ticket image modification options still be null, this can never occurs");
    }

    inline void checkManualOperationsTableMutables(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable)
    {
        assert_msg(updatedJobTicketTable,"job ticket table is null, this can never occurs");
        if(updatedJobTicketTable->pipelineOptions.getMutable() == nullptr)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipeline options property object is null, is need to create a new here");
            updatedJobTicketTable->pipelineOptions = *(std::make_unique<dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable>());
            updatedJobTicketTable->pipelineOptions.getMutable()->beginMergePatch();
        }
        assert_msg(updatedJobTicketTable->pipelineOptions.getMutable(),"job ticket table pipeline options still be null, this can never occurs");
        if(updatedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations.getMutable() == nullptr)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP manual user operations object is null, is need to create a new here");            
            updatedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations = *(std::make_unique<dune::cdm::jobTicket_1::ManualUserOperationsTable>());
            updatedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations.beginMergePatch();
        }
        assert_msg(updatedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations.getMutable(),"job ticket manualUserOperations options still be null, this can never occurs");        
    }

    inline void checkScalingTableMutables(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable)
    {
        assert_msg(updatedJobTicketTable,"job ticket table is null, this can never occurs");
        if(updatedJobTicketTable->pipelineOptions.getMutable() == nullptr)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP pipeline options property object is null, is need to create a new here");
            updatedJobTicketTable->pipelineOptions = *(std::make_unique<dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable>());
            updatedJobTicketTable->pipelineOptions.getMutable()->beginMergePatch();
        }
        assert_msg(updatedJobTicketTable->pipelineOptions.getMutable(),"job ticket table pipeline options still be null, this can never occurs");
        if(updatedJobTicketTable->pipelineOptions.getMutable()->scaling.getMutable() == nullptr)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP scaling property object is null, is need to create a new here");            
            updatedJobTicketTable->pipelineOptions.getMutable()->scaling = *(std::make_unique<dune::cdm::jobTicket_1::ScalingTable>());
            updatedJobTicketTable->pipelineOptions.getMutable()->scaling.beginMergePatch();
        }
        assert_msg(updatedJobTicketTable->pipelineOptions.getMutable()->scaling.getMutable(),"job ticket scaling options still be null, this can never occurs");        
    }

    inline void checkPrintTableMutables(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable)
    {
        assert_msg(updatedJobTicketTable,"job ticket table is null, this can never occurs");
        if(updatedJobTicketTable->dest.getMutable() == nullptr)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP dest property object is null, is need to create a new here");
            updatedJobTicketTable->dest = *(std::make_unique<dune::cdm::jobTicket_1::jobTicket::DestTable>());
            updatedJobTicketTable->dest.getMutable()->beginMergePatch();
        }
        assert_msg(updatedJobTicketTable->dest.getMutable(),"job ticket dest pipeline options still be null, this can never occurs");
        if(updatedJobTicketTable->dest.getMutable()->print.getMutable() == nullptr)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP print property object is null, is need to create a new here");            
            updatedJobTicketTable->dest.getMutable()->print = *(std::make_unique<dune::cdm::jobTicket_1::PrintTable>());
            updatedJobTicketTable->dest.getMutable()->print.beginMergePatch();
        }
        assert_msg(updatedJobTicketTable->dest.getMutable(),"job ticket print options still be null, this can never occurs");
    }

    // ? Could be settings that are not supported on future, add any new if its needed for constraint auto adjust reach the case on future
    static std::unordered_map<std::string, std::function<bool(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)>> MAP
    {
        {
            "src/scan/colorMode",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable);                
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->colorMode);
            }
        },
        {
            "src/scan/mediaSource",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->mediaSource);
            }
        },
        {
            "src/scan/mediaSize",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->mediaSize);
            }
        },
        {
            "src/scan/xOffset",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->xOffset);
            }
        },
        {
            "src/scan/yOffset",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->yOffset);
            }
        },
        {
            "src/scan/plexMode",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->plexMode);
            }
        },
        {
            "src/scan/resolution",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->resolution);
            }
        },
        {
            "src/scan/pageBinding",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->pageBinding);
            }
        },
        {
            "src/scan/contentType",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->contentType);
            }
        },
        {
            "src/scan/contentOrientation",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->contentOrientation);
            }
        },
        {
            "src/scan/pagesFlipUpEnabled",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->pagesFlipUpEnabled);
            }
        },
        {
            "src/scan/autoColorDetect",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->autoColorDetect);
            }
        },
        {
            "src/scan/blackBackground",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->blackBackground);
            }
        },
         {
            "src/scan/mediaType",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->mediaType);
            }
        },
        {
            "src/scan/autoExposure",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->autoExposure);
            }
        },
        {
            "src/scan/gamma",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->gamma);
            }
        },
        {
            "src/scan/highlight",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->highlight);
            }
        },
        {
            "src/scan/colorSensitivity",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->colorSensitivity);
            }
        },
        {
            "src/scan/colorRange",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->colorRange);
            }
        },
        {
            "src/scan/ccdChannel",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->ccdChannel);
            }
        },
        {
            "src/scan/binaryRendering",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->binaryRendering);
            }
        },
        {
            "src/scan/descreen",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->descreen);
            }
        },
        {
            "src/scan/feederPickStop",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->feederPickStop);
            }
        },
        {
            "src/scan/shadow",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->shadow);
            }
        },
        {
            "src/scan/compressionFactor",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->compressionFactor);
            }
        },
        {
            "src/scan/threshold",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->threshold);
            }
        },
        {
            "src/scan/scanCaptureMode",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->scanCaptureMode);
            }
        },
        {
            "src/scan/scanAcquisitionsSpeed",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->scanAcquisitionsSpeed);
            }
        },
        {
            "src/scan/autoDeskew",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->autoDeskew);
            }
        },
        {
            "src/scan/edgeToEdgeScan",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->edgeToEdgeScan);
            }
        },
        {
            "src/scan/longPlotScan",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->longPlotScan);
            }
        },
        {
            "src/scan/invertColors",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScanTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->invertColors);
            }
        },
        {
            "pipelineOptions/imageModifications/sharpness",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->sharpness);
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundCleanup",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->backgroundCleanup);
            }
        },
        {
            "pipelineOptions/imageModifications/exposure",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->exposure);
            }
        },
        {
            "pipelineOptions/imageModifications/contrast",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->contrast);
            }
        },
        {
            "pipelineOptions/imageModifications/blankPageSuppressionEnabled",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->blankPageSuppressionEnabled);
            }
        },
        {
            "pipelineOptions/imageModifications/pagesPerSheet",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->pagesPerSheet);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasMediaSize",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->outputCanvasMediaSize);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasMediaId",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->outputCanvasMediaId);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasCustomWidth",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->outputCanvasCustomWidth);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasCustomLength",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->outputCanvasCustomLength);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasAnchor",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->outputCanvasAnchor);
            }
        },
        {
            "pipelineOptions/imageModifications/outputCanvasOrientation",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->outputCanvasOrientation);
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundNoiseRemoval",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->backgroundNoiseRemoval);
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundColorRemoval",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->backgroundColorRemoval);
            }
        },
        {
            "pipelineOptions/imageModifications/backgroundColorRemovalLevel",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable); 
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->backgroundColorRemovalLevel);
            }
        },
        {
            "pipelineOptions/imageModifications/blackEnhancementLevel",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkImageModificationsTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->blackEnhancementLevel);
            }
        },
        {
            "pipelineOptions/manualUserOperations/imagePreviewConfiguration",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkManualOperationsTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations.getMutable()->imagePreviewConfiguration);
            }
        },
        {
            "pipelineOptions/manualUserOperations/autoRelease",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkManualOperationsTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations.getMutable()->autoRelease);
            }
        },
        {
            "pipelineOptions/scaling/scaleToFitEnabled",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScalingTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->scaling.getMutable()->scaleToFitEnabled);
            }
        },
        {
            "pipelineOptions/scaling/xScalePercent",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScalingTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->scaling.getMutable()->xScalePercent);
            }
        },
        {
            "pipelineOptions/scaling/yScalePercent",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScalingTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->scaling.getMutable()->yScalePercent);
            }
        },
        {
            "pipelineOptions/scaling/scaleSelection",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScalingTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->scaling.getMutable()->scaleSelection);
            }
        },
        {
            "pipelineOptions/scaling/scaleToOutput",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScalingTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->scaling.getMutable()->scaleToOutput);
            }
        },
        {
            "pipelineOptions/scaling/scaleToSize",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkScalingTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->pipelineOptions.getMutable()->scaling.getMutable()->scaleToSize);
            }
        },
        {
            "dest/print/collate",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->collate);
            }
        },
        {
            "dest/print/colorMode",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->colorMode);
            }
        },
        {
            "dest/print/copies",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->copies);
            }
        },
        {
            "dest/print/mediaSource",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->mediaSource);
            }
        },
        {
            "dest/print/mediaDestination",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->mediaDestination);
            }
        },
        {
            "dest/print/mediaSize",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->mediaSize);
            }
        },
        {
            "dest/print/mediaType",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->mediaType);
            }
        },
        {
            "dest/print/foldingStyleId",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->foldingStyleId);
            }
        },
        {
            "dest/print/plexMode",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->plexMode);
            }
        },
        {
            "dest/print/duplexBinding",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->duplexBinding);
            }
        },
        {
            "dest/print/printQuality",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->printQuality);
            }
        },
        {
            "dest/print/resolution",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->resolution);
            }
        },
        {
            "dest/print/printingOrder",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->printingOrder);
            }
        },
        {
            "dest/print/mediaFamily",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->mediaFamily);
            }
        },
        {
            "dest/print/rotate",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->rotate);
            }
        },
        {
            "dest/print/printMargins",
            [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
            { 
                checkPrintTableMutables(updatedJobTicketTable);
                return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->dest.getMutable()->print.getMutable()->printMargins);
            }
        }
    };

    inline bool executeMapFunction(std::string cdmSettingString,
                                const std::shared_ptr<JobTicketTable>& updatedJobTicketTable,
                                std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
    {
        auto pair = Map2UpdateTableProperty::MAP.find(cdmSettingString);
        assert_msg(pair != Map2UpdateTableProperty::MAP.end(),"Unsupported setting %s on updated map expected, return as error", cdmSettingString.c_str());
        return pair->second(updatedJobTicketTable, currentConstraints);
    }
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif // DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_LARGE_FORMAT_MAPPER_H