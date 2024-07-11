package org.newsapp.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.time.ZonedDateTime;

@RequiredArgsConstructor
@Getter
@Entity
public class TaskRun {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne
    private Task task;
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private String status;
    private ZonedDateTime createdAt;

    @PrePersist
    public void prePersist() {
        
    }
}

