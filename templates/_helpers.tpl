{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "locust-replicas.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "locust-replicas.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "locust-replicas.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "locust-replicas.labels" -}}
role: locust-slave
helm.sh/chart: {{ include "locust-replicas.chart" . }}
app.kubernetes.io/name: {{ include "locust-replicas.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "locust-replicas.selectorLabels" -}}
app.kubernetes.io/name: {{ include "locust-replicas.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Locust Master labels
*/}}
{{- define "locust-replicas.labelsMaster" -}}
helm.sh/chart: {{ include "locust-replicas.chart" . }}
{{ include "locust-replicas.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Selector Master labels
*/}}
{{- define "locust-replicas.selectorLabelsMaster" -}}
app.kubernetes.io/name: {{ include "locust-replicas.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
role: locust-master
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "locust-replicas.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "locust-replicas.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Generate Optional Operation for locust Master
*/}}
{{- define "locust-replicas.options-master" -}}
{{- join " " .Values.master.locustOpt | quote }}
{{- end -}}

{{/*
Generate Optional Operation for locust Worker
*/}}
{{- define "locust-replicas.options-worker" -}}
{{- join " " .Values.slave.locustOpt | quote }}
{{- end -}}