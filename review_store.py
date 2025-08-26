# review_store.py — simple TF‑IDF index for product reviews
from __future__ import annotations
import io, csv, logging, os
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger("mymuse")

CSV_HEADERS = ("product_name", "text")

@dataclass
class _Doc:
    product_name: str
    text: str

class ReviewIndex:
    """
    In‑memory TF‑IDF store for quick 'find relevant reviews' by product & query.
    Use:
      ReviewIndex.import_csv(file_or_bytes)   # CSV headers: product_name,text
      ReviewIndex.build()
      ReviewIndex.search("Dive+", transcript_text, k=6)
    """
    _docs: List[_Doc] = []
    _vec: Optional[TfidfVectorizer] = None
    _X = None

    @classmethod
    def import_csv(cls, file_obj) -> Dict:
        """Merge CSV rows into the corpus. Accepts FileStorage or bytes/str buffer."""
        if hasattr(file_obj, "read"):
            raw = file_obj.read()
            # reset for frameworks that reuse stream
            try:
                file_obj.seek(0)
            except Exception:
                pass
        else:
            raw = file_obj
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="ignore")
        buf = io.StringIO(raw)

        reader = csv.DictReader(buf)
        fieldnames = reader.fieldnames or []
        
        # INTELLIGENT CSV FORMAT DETECTION
        added = 0
        
        # Format 1: Standard review format (product_name, text)
        if "product_name" in fieldnames and "text" in fieldnames:
            for row in reader:
                p = (row.get("product_name") or "").strip()
                t = (row.get("text") or "").strip()
                if not t:
                    continue
                cls._docs.append(_Doc(product_name=p, text=t))
                added += 1
        
        # Format 2: Product features format (product_name, features, specs, etc.)
        elif "product_name" in fieldnames and "features" in fieldnames:
            for row in reader:
                p = (row.get("product_name") or "").strip()
                if not p:
                    continue
                
                # Build comprehensive product description from all available fields
                description_parts = []
                
                # Add category if available
                if "category" in fieldnames and row.get("category"):
                    description_parts.append(f"Category: {row['category']}")
                
                # Add control type if available
                if "control_type" in fieldnames and row.get("control_type"):
                    description_parts.append(f"Control: {row['control_type']}")
                
                # Add app features if available
                if "app_features" in fieldnames and row.get("app_features"):
                    description_parts.append(f"App Features: {row['app_features']}")
                
                # Add primary use if available
                if "primary_use" in fieldnames and row.get("primary_use"):
                    description_parts.append(f"Primary Use: {row['primary_use']}")
                
                # Add features if available
                if "features" in fieldnames and row.get("features"):
                    description_parts.append(f"Features: {row['features']}")
                
                # Add specifications if available
                specs_parts = []
                if "specs_run_time_hours" in fieldnames and row.get("specs_run_time_hours"):
                    specs_parts.append(f"Runtime: {row['specs_run_time_hours']} hours")
                if "specs_waterproof_rating" in fieldnames and row.get("specs_waterproof_rating"):
                    specs_parts.append(f"Waterproof: {row['specs_waterproof_rating']}")
                if "specs_max_volume_db" in fieldnames and row.get("specs_max_volume_db"):
                    specs_parts.append(f"Max Volume: {row['specs_max_volume_db']} dB")
                if "specs_charge_time_hours" in fieldnames and row.get("specs_charge_time_hours"):
                    specs_parts.append(f"Charge Time: {row['specs_charge_time_hours']} hours")
                if "battery_mAh" in fieldnames and row.get("battery_mAh"):
                    specs_parts.append(f"Battery: {row['battery_mAh']} mAh")
                if "voltage" in fieldnames and row.get("voltage"):
                    specs_parts.append(f"Voltage: {row['voltage']}")
                if "dimensions_or_size" in fieldnames and row.get("dimensions_or_size"):
                    specs_parts.append(f"Size: {row['dimensions_or_size']}")
                if "materials" in fieldnames and row.get("materials"):
                    specs_parts.append(f"Materials: {row['materials']}")
                
                if specs_parts:
                    description_parts.append(f"Specifications: {'; '.join(specs_parts)}")
                
                # Add how to use if available
                if "how_to_use" in fieldnames and row.get("how_to_use"):
                    description_parts.append(f"Usage: {row['how_to_use']}")
                
                # Combine all parts into a comprehensive text
                if description_parts:
                    combined_text = f"{p} - {' '.join(description_parts)}"
                    cls._docs.append(_Doc(product_name=p, text=combined_text))
                    added += 1
        
        # Format 3: Generic CSV with any structure - try to extract meaningful text
        else:
            for row in reader:
                # Find the first non-empty text field
                text_content = ""
                product_name = "Unknown Product"
                
                for field, value in row.items():
                    if value and value.strip():
                        if "product" in field.lower() or "name" in field.lower():
                            product_name = value.strip()
                        elif len(value.strip()) > 10:  # Only use substantial text fields
                            text_content = value.strip()
                            break
                
                if text_content:
                    cls._docs.append(_Doc(product_name=product_name, text=text_content))
                    added += 1

        total = len(cls._docs)
        logger.info("Imported %d reviews (total=%d)", added, total)
        return {"added": added, "total": total}

    # --------------- Convenience loaders ---------------
    @classmethod
    def import_csv_file(cls, path: str) -> Dict:
        """Import reviews from a CSV file on disk (utf-8)."""
        try:
            if not path or not os.path.exists(path):
                return {"added": 0, "total": len(cls._docs)}
            with open(path, "rb") as f:
                info = cls.import_csv(f)
            logger.info("Loaded reviews CSV: %s (added=%d, total=%d)", path, info.get("added", 0), info.get("total", 0))
            return info
        except Exception as e:
            logger.exception("Failed to import CSV file %s: %s", path, e)
            return {"added": 0, "total": len(cls._docs)}

    @classmethod
    def import_csv_dir(cls, dir_path: str) -> Dict:
        """Import all .csv files in a directory (non-recursive)."""
        total_added = 0
        if not dir_path or not os.path.isdir(dir_path):
            return {"added": 0, "total": len(cls._docs)}
        for name in os.listdir(dir_path):
            if not name.lower().endswith(".csv"):
                continue
            p = os.path.join(dir_path, name)
            info = cls.import_csv_file(p)
            total_added += int(info.get("added", 0))
        return {"added": total_added, "total": len(cls._docs)}

    @classmethod
    def build(cls) -> None:
        """Build TF‑IDF matrix; safe when empty."""
        texts = [d.text for d in cls._docs if d.text.strip()]
        if not texts:
            cls._vec = None
            cls._X = None
            logger.warning("ReviewIndex: no texts to build; index cleared.")
            return
        try:
            vec = TfidfVectorizer(max_features=8000, ngram_range=(1,2), min_df=1)
            X = vec.fit_transform(texts)
            cls._vec, cls._X = vec, X
            logger.info("ReviewIndex built: %d docs, %d terms", len(texts), X.shape[1])
        except Exception as e:
            # Never crash generation because of bad CSV
            logger.exception("ReviewIndex build failed: %s", e)
            cls._vec = None
            cls._X = None

    @classmethod
    def get(cls):  # convenience for warm-up
        return cls

    @classmethod
    def stats(cls) -> Dict:
        by_product: Dict[str, int] = {}
        for d in cls._docs:
            key = d.product_name or "(unspecified)"
            by_product[key] = by_product.get(key, 0) + 1
        products = [{"name": k, "count": v} for k, v in sorted(by_product.items())]
        return {"total_docs": len(cls._docs), "products": products}

    @classmethod
    def samples(cls, n: int = 6) -> List[Dict]:
        out = []
        for d in cls._docs[:max(0, n)]:
            out.append({"product_name": d.product_name, "text": d.text})
        return out

    @classmethod
    def search(cls, product_name: str, query: str, k: int = 6) -> List[str]:
        """
        Return up to k review snippets relevant to (product_name, query).
        If product_name is non-empty, prefer those docs; otherwise search all.
        """
        if not cls._vec or cls._X is None or not cls._docs:
            return []
        # Choose candidate indices by product
        cand_idx = [i for i, d in enumerate(cls._docs) if (product_name and d.product_name and d.product_name.lower() == product_name.lower())]
        if not cand_idx:
            cand_idx = list(range(len(cls._docs)))
        if not cand_idx:
            return []

        # Vectorize query
        try:
            qv = cls._vec.transform([query or ""])
        except Exception:
            return []
        # Compute similarities on the candidate subset
        import numpy as np
        subX = cls._X[cand_idx, :]
        sims = cosine_similarity(qv, subX).ravel()  # shape (len(cand_idx),)
        # Top-k
        top_local = np.argsort(-sims)[:k]
        results = []
        for j in top_local:
            i = cand_idx[j]
            txt = cls._docs[i].text.strip()
            if txt:
                results.append(txt)
        return results
