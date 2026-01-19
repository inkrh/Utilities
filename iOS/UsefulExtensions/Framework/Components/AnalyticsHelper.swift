//analytics helper class to hit GA without needing to use Google Analytics libraries
//see https://developers.google.com/analytics/devguides/collection/protocol/v1/reference
//uses POST not GET for sending data

import Foundation

public class AnalyticsHelper {
    //anonymous UserID per app installation - purposefully not tied into any other system
    //could be improved a lot here
    private class UserID {
        let key = "UUID"

        init() {
            _ = getUserId()
        }
        
        func getUserId() -> String {
            if (UserDefaults.standard.object(forKey: key) != nil) {
                return UserDefaults.standard.object(forKey: key) as! String
            }
            return setUserId()
        }


        func setUserId() -> String {
            let uid = UUID().uuidString
            UserDefaults.standard.set(uid, forKey: key)
            UserDefaults.standard.synchronize()
            return uid
        }

    }
    
    private func POST(event: String, eventAction: String, eventLabel: String, eventValue: Int, instanceId: String) {
        let CID: String = UserID.init().getUserId()
        let urlString: String = "https://www.google-analytics.com/collect" //leveraging GA measurement endpoint
        guard
            let url = URL(string: urlString) else {
            RSLog(urlString + "FAILED")
            return

        }
        var request = URLRequest(url: url)
        request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"
        //request format:
        //v=protocol version
        //tid=tracking id
        //cid=unique user id
        //t=hit type
        //ec=event name
        //ea=event action
        //el=event label
        //ev=event value
        let parameters = "v=1&t=event&tid=" + instanceId + "&cid=" + CID + "&ec=" + event + "&ea=" + eventAction + "&el=" + eventLabel + "&ev="+String(eventValue)

        request.httpBody = parameters.data(using: .utf8)

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data,
                  let response = response as? HTTPURLResponse,
                  error == nil else {
                RSLog(error ?? "Error in analytics request")
                return
            }

            guard (200...299) ~= response.statusCode else {                    // check for http errors
                RSLog( "statusCode should be 2xx, but is \(response.statusCode)")
                RSLog( "response = \(response)")
                return
            }

            let responseString = String(data: data, encoding: .utf8)
            RSLog("responseString = \(responseString)")
        }

        task.resume()
    }

    
    
    public func SendEvent(instanceId: String, event:String, eventAction: String, eventLabel:String, eventValue: Int) {
        POST(event: event, eventAction: eventAction, eventLabel: eventLabel, eventValue: eventValue, instanceId: instanceId)
    }


    public func SendEvent(instanceId: String, event: String) {
        SendEvent(instanceId: instanceId, event:event, eventAction: "", eventLabel: "", eventValue: 0)
    }

    public func SendEvent(instanceId: String, event: String, eventAction: String) {
        SendEvent(instanceId: instanceId, event:event, eventAction: eventAction, eventLabel: "", eventValue: 0)
    }

    public func SendEvent(instanceId: String, event: String, eventAction: String, evenLabel:String) {
        SendEvent(instanceId: instanceId, event:event, eventAction: eventAction, eventLabel: evenLabel, eventValue: 0)
    }
    
    
}


