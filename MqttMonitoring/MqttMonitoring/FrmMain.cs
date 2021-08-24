using MySql.Data.MySqlClient;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Net;
using System.Text;
using System.Windows.Forms;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace MqttSubscriber
{
    public partial class FrmMain : Form
    {
        MqttClient client;
        private string connectionString;
        private ulong line_count;
        private float open_temp, close_temp;
        private bool opened;

        delegate void UpdateTextCallback(string message);

        public FrmMain()
        {
            InitializeComponent();
            InitAllData();
        }

        private void InitAllData()
        {
            connectionString = "Server=localhost;Port=3306;" +
                                "Database=iot_data;Uid=root;Pwd=maria_p@ssw0rd!";
            line_count = 0;
            BtnConnect.Enabled = true;
            BtnDisconnect.Enabled = false;

            var temps = TxtControlTemp.Text.Split(',');
            opened = false; // 모터 컨트롤로 오픈했는지? 
            open_temp = float.Parse(temps[0].Trim());
            close_temp = float.Parse(temps[1].Trim());
            UpdateText($"Initialized - Open Temperature {open_temp}°C / Close Temperature {close_temp}°C");
        }

        private void FrmMain_Load(object sender, EventArgs e)
        {
            try
            {
                IPAddress hostIP;
                hostIP = IPAddress.Parse(TxtConnectionString.Text);
                client = new MqttClient(hostIP);

                client.MqttMsgPublishReceived += Client_MqttMsgPublishReceived;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void Client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            try
            {
                var message = Encoding.UTF8.GetString(e.Message);
                UpdateText(">>> Message: " + message);
                InsertData(message);        // 메시지가 발생할 경우 DB에 저장
                SendToBroker(message);      // 알람이 발생시 디바이스로 재전송
            }
            catch (Exception ex)
            {
                UpdateText("[ERROR] " + ex.Message);
            }
        }

        private void SendToBroker(string message)
        {
            var currentDatas = JsonConvert.DeserializeObject<Dictionary<string, string>>(message);

            var dev_id = currentDatas["dev_id"];
            var currTemp = float.Parse(currentDatas["temp"]);
            Debug.WriteLine(currTemp);

            JObject json = new JObject();
            if (currTemp >= open_temp)
            {
                if (opened == false)
                {
                    json.Add("dev_id", dev_id);
                    json.Add("state", "ON");
                    string strJson = JsonConvert.SerializeObject(json);
                    client.Publish(TxtPayload.Text, Encoding.Default.GetBytes(strJson));
                    Debug.WriteLine(json);

                    opened = true;
                    UpdateText($"{dev_id} state Alarm");
                }                
                
            }
            else if (currTemp <= close_temp)
            {
                if (opened)
                {
                    json.Add("dev_id", dev_id);
                    json.Add("state", "OFF");
                    string strJson = JsonConvert.SerializeObject(json);
                    client.Publish(TxtPayload.Text, Encoding.Default.GetBytes(strJson));
                    Debug.WriteLine(json);

                    opened = false;
                    UpdateText($"{dev_id} state Normal");
                }
                
            }
        }

        private void InsertData(string message)
        {
            var currentDatas = JsonConvert.DeserializeObject<Dictionary<string, string>>(message);
            using (var conn = new MySqlConnection(connectionString))
            {
                string strInsertQry = string.Format("INSERT INTO iot_data.sensordata " +
                                        " (idx, dev_id, time, temp, humid) " +
                                        "VALUES (NULL, '{0}', '{1}', {2}, {3}); ",
                                        currentDatas["dev_id"], currentDatas["time"],
                                        currentDatas["temp"], currentDatas["humid"]);
                try
                {
                    conn.Open();
                    MySqlCommand cmd = new MySqlCommand(strInsertQry, conn);
                    if (cmd.ExecuteNonQuery() == 1)
                        UpdateText("[DB] " + "Insert succeed");
                    else
                        UpdateText("[DB] " + "Insert failed");
                }
                catch (Exception ex)
                {
                    UpdateText("[DB] " + ex.Message);
                }
            }
        }

        private void UpdateText(string message)
        {
            if (RtbRecieved.InvokeRequired)
            {
                UpdateTextCallback d = new UpdateTextCallback(UpdateText);
                this.Invoke(d, new object[] { message });
            }
            else
            {
                line_count++;
                this.RtbRecieved.AppendText(line_count.ToString() + " : " + message + "\n");
                this.RtbRecieved.ScrollToCaret();
            }
        }

        private void BtnConnect_Click(object sender, EventArgs e)
        {
            try
            {
                client.Connect(TxtClientId.Text + "_sub");
                UpdateText(">>>>> Client connected");
                client.Subscribe(new string[] { TxtTopic.Text }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE });
                UpdateText(">>>>> Subscribing to : " + TxtTopic.Text);

                BtnConnect.Enabled = false;
                BtnDisconnect.Enabled = true;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());

                BtnConnect.Enabled = true;
                BtnDisconnect.Enabled = false;
            }
        }

        private void BtnDisconnect_Click(object sender, EventArgs e)
        {
            try
            {
                client.Disconnect();
                UpdateText(">> Client disconnected");

                BtnConnect.Enabled = true;
                BtnDisconnect.Enabled = false;

            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());

                BtnConnect.Enabled = false;
                BtnDisconnect.Enabled = true;
            }
        }
    }
}
