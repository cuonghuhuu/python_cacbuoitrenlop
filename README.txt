HƯỚNG DẪN CHẠY

1. Cài thư viện:
   pip install -r requirements.txt

2. Đặt 2 file cùng thư mục:
   - main.py
   - hr_manager.ui

3. Chạy chương trình:
   python main.py

GHI CHÚ QUAN TRỌNG
- Code này giả định CSDL PostgreSQL có 2 bảng:
  department(department_id, department_name, manager_id, location_id)
  employee(employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id)

- Nếu bảng của bạn là employees/departments hoặc tên cột khác, hãy sửa lại câu SQL trong main.py.
- Mục A đang lọc theo job_id có chứa MAN / MGR. Nếu schema của bạn có bảng jobs riêng, bạn có thể đổi truy vấn cho phù hợp.
