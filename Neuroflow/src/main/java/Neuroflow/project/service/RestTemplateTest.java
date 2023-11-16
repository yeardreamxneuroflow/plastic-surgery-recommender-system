package Neuroflow.project.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.io.File;

@Service
public class RestTemplateTest {

    public String postApiTest() {
        RestTemplate restTemplate = new RestTemplate();

        File file = new File("static/images/testImg.jpeg");



//        byte[] response = restTemplate.postForObject("", byte[].class);
        return "12345";
    }
}
