#ifndef DUNE_JOB_COPYPAGERESULT_H
#define DUNE_JOB_COPYPAGERESULT_H
////////////////////////////////////////////////////////////////////////////////
/**
 * @file  CopyPageResult.h
 * @brief Dune Job Pipeline - CopyPageResult Class Definition
 * @date  April 14th, 2023
 *
 * (c) Copyright HP Inc. 2023. All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "CopyPageResult_generated.h"
#include "PrintPageResult.h"
#include "ScanPageResult.h"

namespace dune { namespace job {
/**
 * @class CopyPageResult
 */

class CopyPageResult
{
    public:
      CopyPageResult() :
        printPageResult_{std::make_shared<dune::job::PrintPageResult>()},
        scanPageResult_{std::make_shared<dune::job::ScanPageResult>()}
        {
        }
    
        inline std::shared_ptr<dune::job::PrintPageResult> getPrintPageResult() { return printPageResult_;}
        inline std::shared_ptr<dune::job::ScanPageResult>  getScanPageResult()  { return scanPageResult_;}

      /**
       * @brief Serialize / Deserialize Copy Page Ticket from/to FlatBuffer struct
       *
       * @return std::unique_ptr<CopyPageTicketFbT> Serialized Copy Page Ticket to FlatBuffer struct
       */
      inline std::unique_ptr<CopyPageResultFbT> serializeToFb() const
      {
        std::lock_guard<std::recursive_mutex> lock_(mutex_);

        std::unique_ptr<dune::job::CopyPageResultFbT> copyPageResultFb{std::make_unique<dune::job::CopyPageResultFbT>()};
        if (printPageResult_)
        {
          copyPageResultFb->printPageResult = printPageResult_->serializeResult();
        }
        if (scanPageResult_)
        {
          copyPageResultFb->scanPageResult = scanPageResult_->serializeResult();
        }

        return copyPageResultFb;
      }

      inline void deserializeFromFb(const CopyPageResultFbT& copyPageResultFb)
      {
        std::lock_guard<std::recursive_mutex> lock_(mutex_);

        printPageResult_->deserializeResult(*copyPageResultFb.printPageResult);
        scanPageResult_->deserializeResult(*copyPageResultFb.scanPageResult);
      }

    private:
      std::shared_ptr<dune::job::PrintPageResult> printPageResult_{nullptr};
      std::shared_ptr<dune::job::ScanPageResult> scanPageResult_{nullptr};
      mutable std::recursive_mutex mutex_;
};

}}

#endif // DUNE_JOB_COPYPAGERESULT_H