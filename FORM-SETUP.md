# Nối form đăng ký tư vấn vào Google Sheet

Trang là HTML tĩnh nên dùng **Google Apps Script Web App** làm nơi nhận đơn và ghi vào Google Sheet.
Làm 1 lần, miễn phí, không cần server.

## Bước 1 — Tạo Google Sheet
1. Vào https://sheets.new tạo bảng mới, đặt tên ví dụ **"Đơn tư vấn - Thành Công Clinic"**.
2. Không cần tạo cột tay; script sẽ tự tạo dòng tiêu đề ở lần ghi đầu tiên.

## Bước 2 — Dán Apps Script
1. Trong Sheet: menu **Extensions → Apps Script**.
2. Xóa code mẫu, dán đoạn dưới đây, rồi **Save** (biểu tượng đĩa).

```javascript
function doPost(e) {
  try {
    var lock = LockService.getScriptLock();
    lock.waitLock(20000);

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('DonTuVan') || ss.getActiveSheet();

    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        'Thời gian', 'Tên doanh nghiệp', 'Địa chỉ', 'Người liên hệ',
        'Số điện thoại', 'Số lượng nhân viên', 'Nội dung yêu cầu'
      ]);
    }

    var p = e.parameter || {};
    sheet.appendRow([
      new Date(),
      p.company  || '',
      p.address  || '',
      p.contact  || '',
      p.phone    || '',
      p.employees|| '',
      p.message  || ''
    ]);

    lock.releaseLock();
    return ContentService
      .createTextOutput(JSON.stringify({ result: 'success' }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ result: 'error', error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

## Bước 3 — Deploy thành Web App
1. Góc phải trên: **Deploy → New deployment**.
2. Chọn loại (bánh răng) **Web app**.
3. Cấu hình:
   - **Execute as:** `Me` (tài khoản của bạn)
   - **Who has access:** `Anyone`  ← bắt buộc để website gọi được
4. Bấm **Deploy**, cấp quyền (Authorize access) khi được hỏi.
5. Copy **Web app URL** dạng `https://script.google.com/macros/s/AKfy.../exec`.

> Mỗi lần sửa code phải **Deploy → Manage deployments → chỉnh (bút chì) → Version: New version → Deploy**
> để cập nhật. URL `/exec` giữ nguyên.

## Bước 4 — Gắn URL vào website
Mở `index.html`, tìm dòng:

```javascript
const FORM_ENDPOINT = 'PASTE_APPS_SCRIPT_WEB_APP_URL_HERE';
```

Thay bằng URL `/exec` vừa copy. Lưu lại là xong — đơn sẽ tự động ghi vào Sheet.

(Hoặc gửi URL đó cho mình, mình dán giúp.)

## Kiểm tra
- Điền thử form trên web → mở Google Sheet thấy dòng mới với đầy đủ thông tin + thời gian.
- Khi chưa gắn URL (còn `PASTE_...`), form vẫn chạy ở **chế độ demo**: hiện thông báo thành công
  nhưng KHÔNG ghi đi đâu (để test giao diện).

## Ghi chú
- URL `/exec` chỉ là endpoint ghi-thêm, không chứa mật khẩu, có thể để trong code/commit bình thường.
- Muốn nhận thêm email mỗi khi có đơn: thêm `MailApp.sendEmail('email@vd.com', 'Đơn mới', JSON.stringify(p));`
  vào trong `doPost` trước phần `return`.
