package org.newsapp.domain.task;

import jakarta.persistence.*;
import lombok.Builder;
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
    @JoinColumn(name = "task_id")
    private Task task;
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private TaskRunStatus status;
    private ZonedDateTime createdAt;

    @PrePersist
    public void prePersist() {
        this.createdAt = ZonedDateTime.now();
    }

    public TaskRun(Task task) {
        this.task = task;
        this.status = TaskRunStatus.CREATED;
    }

    public void updateStatus(TaskRunStatus status) {
        this.status = status;
    }
}

