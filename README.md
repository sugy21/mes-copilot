# MES Copilot Project (학생용 템플릿)

이 프로젝트는 **GitHub Copilot 실습용 FastAPI 기반 템플릿**입니다.  
1~8차시 수업에서 동일하게 사용되며, Copilot을 활용해 점진적으로 확장됩니다.

---

## 📁 폴더 구조

app/
├─ main.py
├─ routers/
├─ services/
├─ models/
└─ database/

## ⚙️ 로컬 실행 (1~4차시)
```bash
py -m venv .venv
.venv\Scripts\activate # (Windows)
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```