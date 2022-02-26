use std::sync::atomic::Ordering;

use bytes::Bytes;
use pyo3::prelude::*;
use rq_engine::command::wtlogin::{LoginResponse, QRCodeState};
use rq_engine::Engine;
use rq_engine::protocol::packet::Packet;
use rq_engine::protocol::version::{get_version, Protocol};

use crate::device::PyDevice;
use crate::packet::PyPacket;
use crate::pbytes::PBytes;

#[pyclass(name = "Engine")]
pub struct PyEngine {
    pub inner: Engine,
}

#[pymethods]
impl PyEngine {
    #[new]
    fn new(device: PyDevice, protocol: i32) -> Self {
        let protocol = match protocol {
            1 => Protocol::AndroidPhone,
            2 => Protocol::AndroidWatch,
            3 => Protocol::MacOS,
            4 => Protocol::QiDian,
            _ => Protocol::IPad
        };
        Self {
            inner: Engine::new(device.into(), get_version(protocol))
        }
    }

    #[getter(uin)]
    fn uin(&self) -> PyResult<i64> {
        Ok(self.inner.uin.load(Ordering::Relaxed))
    }

    #[setter(uin)]
    fn set_uin(&mut self, value: i64) -> PyResult<()> {
        self.inner.uin.store(value, Ordering::Relaxed);
        Ok(())
    }
    /// decode_packet(self, payload: bytes) -> Packet
    /// --
    ///
    /// decode packet
    fn decode_packet(&self, payload: &[u8]) -> PyPacket {
        let pkt = self.inner.transport.decode_packet(payload).unwrap();
        PyPacket::from(pkt)
    }

    /// encode_packet(self, pkt: Packet) -> bytes
    /// --
    ///
    /// encode packet
    fn encode_packet(&self, pkt: PyPacket) -> PBytes {
        let b = self.inner.transport.encode_packet(Packet::from(pkt));
        PBytes(b)
    }

    /// build_qrcode_fetch_request_packet(self) -> Packet
    /// --
    ///
    /// fetch qrcode for login
    fn build_qrcode_fetch_request_packet(&self) -> PyPacket {
        self.inner.build_qrcode_fetch_request_packet().into()
    }

    /// build_heartbeat_packet(self) -> Packet
    /// --
    ///
    /// build heartbeat packet
    fn build_heartbeat_packet(&self) -> PyPacket {
        self.inner.build_heartbeat_packet().into()
    }

    /// build_client_register_packet(self) -> Packet
    /// --
    ///
    /// build client register packet
    fn build_client_register_packet(&self) -> PyPacket {
        self.inner.build_client_register_packet().into()
    }

    /// build_update_signature_packet(self, signature: str) -> Packet
    /// --
    ///
    /// build update signature packet
    fn build_update_signature_packet(&self, signature: &str) -> PyPacket {
        self.inner.build_update_signature_packet(signature.to_string()).into()
    }

    /// decode_trans_emp_response(self, payload: bytes) -> QRCodeState
    /// --
    ///
    /// fetch qrcode for login
    fn decode_trans_emp_response(&mut self, payload: &[u8]) -> PyQRCodeState {
        let resp = self.inner.decode_trans_emp_response(Bytes::from(payload.to_vec())).unwrap();
        match resp {
            QRCodeState::ImageFetch(fetch) => {
                PyQRCodeState {
                    image_fetch: Some(PyQRCodeImageFetch {
                        sig: PBytes(fetch.sig),
                        image: PBytes(fetch.image_data),
                    }),
                    ..Default::default()
                }
            }
            QRCodeState::WaitingForConfirm => {
                PyQRCodeState {
                    waiting_for_confirm: Some(true),
                    ..Default::default()
                }
            }
            QRCodeState::WaitingForScan => {
                PyQRCodeState {
                    waiting_for_scan: Some(true),
                    ..Default::default()
                }
            }
            QRCodeState::Timeout => {
                PyQRCodeState {
                    timeout: Some(true),
                    ..Default::default()
                }
            }
            QRCodeState::Canceled => {
                PyQRCodeState {
                    canceled: Some(true),
                    ..Default::default()
                }
            }
            QRCodeState::Confirmed(confirmed) => {
                self.inner.process_qrcode_confirmed(confirmed.clone());
                self.inner.uin.store(confirmed.uin, Ordering::Relaxed);
                PyQRCodeState {
                    confirmed: Some(PyQRCodeConfirmed {
                        uin: confirmed.uin,
                        tmp_pwd: PBytes(confirmed.tmp_pwd),
                        tmp_no_pic_sig: PBytes(confirmed.tmp_no_pic_sig),
                        tgt_qr: PBytes(confirmed.tgt_qr),
                        ..Default::default()
                    }),
                    ..Default::default()
                }
            }
        }
    }

    /// build_qrcode_result_query_request_packet(self, sig: bytes) -> Packet
    /// --
    ///
    /// build qrcode result query request packet
    fn build_qrcode_result_query_request_packet(&self, sig: &[u8]) -> PyPacket {
        self.inner.build_qrcode_result_query_request_packet(sig).into()
    }

    /// build_qrcode_login_packet(self, t106: bytes, t16a: bytes, t318: bytes) -> Packet
    /// --
    ///
    /// build qrcode login packet
    fn build_qrcode_login_packet(&self, t106: &[u8], t16a: &[u8], t318: &[u8]) -> PyPacket {
        self.inner.build_qrcode_login_packet(t106, t16a, t318).into()
    }

    /// build_device_lock_login_packet(self) -> Packet
    /// --
    ///
    /// build device lock login packet
    fn build_device_lock_login_packet(&self) -> PyPacket {
        self.inner.build_device_lock_login_packet().into()
    }

    /// build_login_packet(self, password_md5: bytes) -> Packet
    /// --
    ///
    /// build login packet
    fn build_login_packet(&self, password_md5: &[u8]) -> PyPacket {
        self.inner.build_login_packet(password_md5, true).into()
    }

    /// build_sms_request_packet(self) -> Packet
    /// --
    ///
    /// build sms request packet
    fn build_sms_request_packet(&self) -> PyPacket {
        self.inner.build_sms_request_packet().into()
    }

    /// build_sms_code_submit_packet(self, code: str) -> Packet
    /// --
    ///
    /// build sms code submit packet
    fn build_sms_code_submit_packet(&self, code: &str) -> PyPacket {
        self.inner.build_sms_code_submit_packet(code).into()
    }

    /// build_ticket_submit_packet(self, ticket: str) -> Packet
    /// --
    ///
    /// build ticket submit packet
    fn build_ticket_submit_packet(&self, ticket: &str) -> PyPacket {
        self.inner.build_ticket_submit_packet(ticket).into()
    }

    /// decode_login_response(self, payload: bytes) -> LoginResponse
    /// --
    ///
    /// decode login response
    fn decode_login_response(&mut self, payload: &[u8]) -> PyLoginResponse {
        let resp = self.inner.decode_login_response(Bytes::from(payload.to_vec())).unwrap();
        self.inner.process_login_response(resp.clone());
        match resp {
            LoginResponse::Success(success) => {
                let account_info = success.account_info.unwrap_or_default();
                PyLoginResponse {
                    success: Some(PyLoginSuccess {
                        account_info: PyAccountInfo {
                            nick: account_info.nick,
                            age: account_info.age,
                            gender: account_info.gender,
                        }
                    }),
                    ..Default::default()
                }
            }
            LoginResponse::DeviceLockLogin(_) => PyLoginResponse {
                device_lock_login: Some(true),
                ..Default::default()
            },
            LoginResponse::AccountFrozen => PyLoginResponse {
                account_frozen: Some(true),
                ..Default::default()
            },
            LoginResponse::TooManySMSRequest => PyLoginResponse {
                too_many_sms_request: Some(true),
                ..Default::default()
            },
            LoginResponse::DeviceLocked(device_locked) => PyLoginResponse {
                device_locked: Some(PyLoginDeviceLocked {
                    sms_phone: device_locked.sms_phone,
                    verify_url: device_locked.verify_url,
                    message: device_locked.message,
                }),
                ..Default::default()
            },
            LoginResponse::NeedCaptcha(need_captcha) => PyLoginResponse {
                need_captcha: Some(PyLoginNeedCaptcha {
                    verify_url: need_captcha.verify_url,
                }),
                ..Default::default()
            },
            LoginResponse::UnknownStatus(_) => PyLoginResponse {
                unknown_status: Some(true),
                ..Default::default()
            },
        }
    }

    /// uni_packet(self, command_name: str, body: bytes) -> Packet
    /// --
    ///
    /// uni packet
    fn uni_packet(&self, command_name: &str, body: &[u8]) -> PyPacket {
        self.inner.uni_packet(command_name, Bytes::from(body.to_vec())).into()
    }
}

// 扫码登录
// 假装是 enum
#[pyclass(name = "QRCodeState")]
#[derive(Default, Clone)]
pub struct PyQRCodeState {
    #[pyo3(get, set)]
    pub image_fetch: Option<PyQRCodeImageFetch>,
    #[pyo3(get, set)]
    pub confirmed: Option<PyQRCodeConfirmed>,
    #[pyo3(get, set)]
    pub waiting_for_scan: Option<bool>,
    #[pyo3(get, set)]
    pub waiting_for_confirm: Option<bool>,
    #[pyo3(get, set)]
    pub timeout: Option<bool>,
    #[pyo3(get, set)]
    pub canceled: Option<bool>,
}

#[pyclass(name = "QRCodeImageFetch")]
#[derive(Default, Clone)]
pub struct PyQRCodeImageFetch {
    #[pyo3(get, set)]
    pub sig: PBytes,
    #[pyo3(get, set)]
    pub image: PBytes,
}


#[pyclass(name = "QRCodeConfirmed")]
#[derive(Default, Clone)]
pub struct PyQRCodeConfirmed {
    #[pyo3(get, set)]
    pub uin: i64,
    #[pyo3(get, set)]
    pub tmp_pwd: PBytes,
    #[pyo3(get, set)]
    pub tmp_no_pic_sig: PBytes,
    #[pyo3(get, set)]
    pub tgt_qr: PBytes,
}

// 密码登录
// 假装是 enum
#[pyclass(name = "LoginResponse")]
#[derive(Default, Clone)]
pub struct PyLoginResponse {
    #[pyo3(get, set)]
    pub success: Option<PyLoginSuccess>,
    #[pyo3(get, set)]
    pub device_lock_login: Option<bool>,
    #[pyo3(get, set)]
    pub account_frozen: Option<bool>,
    #[pyo3(get, set)]
    pub too_many_sms_request: Option<bool>,
    #[pyo3(get, set)]
    pub device_locked: Option<PyLoginDeviceLocked>,
    #[pyo3(get, set)]
    pub need_captcha: Option<PyLoginNeedCaptcha>,
    #[pyo3(get, set)]
    pub unknown_status: Option<bool>,
}

#[pyclass(name = "LoginSuccess")]
#[derive(Default, Clone)]
pub struct PyLoginSuccess {
    #[pyo3(get, set)]
    pub account_info: PyAccountInfo,
}

#[pyclass(name = "LoginDeviceLocked")]
#[derive(Default, Clone)]
pub struct PyLoginDeviceLocked {
    #[pyo3(get, set)]
    pub sms_phone: Option<String>,
    #[pyo3(get, set)]
    pub verify_url: Option<String>,
    #[pyo3(get, set)]
    pub message: Option<String>,
}

#[pyclass(name = "LoginNeedCaptcha")]
#[derive(Default, Clone)]
pub struct PyLoginNeedCaptcha {
    #[pyo3(get, set)]
    pub verify_url: Option<String>,
}

#[pyclass(name = "AccountInfo")]
#[derive(Default, Clone)]
pub struct PyAccountInfo {
    #[pyo3(get, set)]
    pub nick: String,
    #[pyo3(get, set)]
    pub age: u8,
    #[pyo3(get, set)]
    pub gender: u8,
}