package org.newsapp.domain.task;

import jakarta.persistence.*;
import lombok.*;
import org.newsapp.dto.task.TaskRequestDTO;

import java.time.ZonedDateTime;
import java.util.List;

@RequiredArgsConstructor
@Getter
@Entity
public class Task {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "id")
    private List<TaskRun> taskRuns;

    @Column(nullable = false, unique = true)
    private String name;

    @Column(nullable = false, unique = true)
    private String keyword;

    private String schedule;

    @Column(nullable = false)
    private Integer days;

    private ZonedDateTime createdAt;

    private ZonedDateTime modifiedAt;

    @Builder
    public Task(String name, String keyword, String schedule, Integer days) {
        this.name = name;
        this.keyword = keyword;
        this.schedule = schedule;
        this.days = days;
    }

    @PrePersist
    public void onPrePersist() {
        this.createdAt = ZonedDateTime.now();
        this.modifiedAt = ZonedDateTime.now();
    }

    @PreUpdate
    public void onPreUpdate() {
        this.modifiedAt = ZonedDateTime.now();
    }

    public void update(TaskRequestDTO request) {
        if (request.getName() != null) {
            this.name = request.getName();
        }
        if (request.getKeyword() != null) {
            this.keyword = request.getKeyword();
        }
        if (request.getSchedule() != null) {
            this.schedule = request.getSchedule();
        }
        if (request.getDays() != null) {
            this.days = request.getDays();
        }
    }

}
