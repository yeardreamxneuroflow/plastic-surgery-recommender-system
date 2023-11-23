package Neuroflow.project.service;

import jakarta.annotation.PostConstruct;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.io.*;
import java.sql.SQLException;

@Service
public class WebClientTest {
    private WebClient webClient;

    @PostConstruct
    public void initWebClient() {
        webClient = WebClient.create("http://13.209.213.35:5000");
    }


    public byte[] verification(MultipartFile multipartFile) {
        webClient = WebClient.create("http://13.209.213.35:5000");

        MultipartBodyBuilder builder = new MultipartBodyBuilder();
        builder.part("img_file", multipartFile.getResource());
        var payloadFile = builder.build();

        return webClient.post()
                .uri("/recommend")
                .contentType(MediaType.MULTIPART_FORM_DATA)
                .body(BodyInserters.fromMultipartData(payloadFile))
                .retrieve()
                .bodyToMono(byte[].class)
                .block();
    }

}
