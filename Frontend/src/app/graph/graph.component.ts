import {Component, ElementRef, HostListener, Input, OnInit, ViewChild} from '@angular/core';
import {JsonHandlerService} from "../service/json-handler.service";
import {Edge, Layout, Node} from "@swimlane/ngx-graph";
import {DagreNodesOnlyLayout} from "@swimlane/ngx-graph"
import * as shape from 'd3-shape';
import {Subject} from "rxjs";

export class QuestionBlock {
  id!: string;
  name!: string;
  upperId?: string;
}
interface CustomNode extends Node {
  isSelected?: boolean;
}
@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss']
})

export class GraphComponent implements OnInit {
  @ViewChild('graph', { static: true }) graph!: ElementRef;
  isDraggingEdge = false;
  public draggingEdge: Edge | null = null;
  update$: Subject<boolean> = new Subject();
  center$: Subject<boolean> = new Subject();
  zoomToFit$: Subject<boolean> = new Subject();
  @Input() questionBlocks: QuestionBlock[] = [];
  public nodes: Node[] = [];
  public links: Edge[] = [];
  public selectedNodes: CustomNode[] = [];
  public layoutSettings = {
    orientation: 'TB'
  };
  public layout: Layout = new DagreNodesOnlyLayout();
  public curve: any = shape.curveLinear;
  constructor(private jsonHandlerService: JsonHandlerService) {
    this.questionBlocks = [
      {
        id: '1',
        name: 'Начало'
      }
    ];
  }

  public ngOnInit() {
    const savedGraphData = this.jsonHandlerService.getGraphDataFromModules();
      if (!savedGraphData || savedGraphData.nodes.length === 0) {
      } else {
          this.nodes = savedGraphData.nodes;
          this.links = savedGraphData.links;
      }
  }
  deleteEdge(link: Edge) {
    const edgeIndex = this.links.findIndex(edge => edge.source === link.source && edge.target === link.target);
    if (edgeIndex !== -1) {
      const deletedEdge = this.links.splice(edgeIndex, 1)[0];
      const jsonData = this.jsonHandlerService.getJsonData() || {};
      if (jsonData && jsonData.journal.modules) {
        const sourceModule = jsonData.journal.modules[deletedEdge.source];
        if (sourceModule) {
          sourceModule.next_id = null;
          this.jsonHandlerService.saveJsonData(jsonData);
        }
      }
      this.updateGraph();
      localStorage.setItem('graphLinks', JSON.stringify(this.links));
    }
  }
  updateGraph() {
    this.update$.next(true)
  }
  centerGraph() {
    this.center$.next(true);
  }
  fitGraph() {
    this.zoomToFit$.next(true)
  }
  private sourceNodeCoordinates: { x: number, y: number } | null = null;
  onNodeClick(selectedNode: CustomNode) {
    const index = this.selectedNodes.findIndex(node => node.id === selectedNode.id);
    if (index != -1) {
      this.selectedNodes.splice(index, 1);
    } else {
      this.selectedNodes.push(selectedNode);
      selectedNode['isSelected'] = true;
    }
    this.createEdgeIfNeeded();
  }
  createEdgeIfNeeded() {
    if (this.selectedNodes.length === 2) {
      const sourceNode = this.selectedNodes[0];
      const targetNode = this.selectedNodes[1];
      const existingEdge = this.links.find(edge => edge.source === sourceNode.id && edge.target === targetNode.id
        || edge.source === targetNode.id && edge.target === sourceNode.id);
      if (!existingEdge && !this.hasExistingNextId(sourceNode.id)) {
        const newEdge: Edge = {
          source: sourceNode.id,
          target: targetNode.id,
          label: ''
        }
        this.links.push(newEdge);
        const jsonData = this.jsonHandlerService.getJsonData() || {};
        if (jsonData && jsonData.journal.modules) {
          const sourceModule = jsonData.journal.modules[sourceNode.id];
          if (sourceModule) {
            sourceModule.next_id = targetNode.id;
            this.jsonHandlerService.saveJsonData(jsonData);
          }
        }
        localStorage.setItem('graphLinks', JSON.stringify(this.links));
        this.updateGraph();
      }
      this.selectedNodes.forEach(node => delete node['isSelected']);
      this.selectedNodes = [];
    }
  }
  private hasExistingNextId(nodeId: string): boolean {
    const jsonData = this.jsonHandlerService.getJsonData() || {};
    const sourceModule = jsonData.journal?.modules?.[nodeId];
    return sourceModule?.next_id !== undefined && sourceModule?.next_id !== null;
  }
  onEdgeDragStart(event: MouseEvent, edge: Edge) {
    this.isDraggingEdge = true;
    this.draggingEdge = edge;
  }
  onEdgeDragEnd() {
    this.isDraggingEdge = false;
    this.draggingEdge = null;
  }
  onNodeMouseOver(node: CustomNode) {
    if (this.isDraggingEdge && this.draggingEdge) {
      const existingEdge = this.links.find(edge => edge.source === this.draggingEdge!.source && edge.target === node.id
      || edge.source === node.id && edge.target === this.draggingEdge!.source);
      if (!existingEdge) {
        const newEdge: Edge = {
          source: this.draggingEdge.source,
          target: node.id,
          label: ''
        };
        const index = this.links.findIndex(edge => edge.source === this.draggingEdge!.source && edge.target === this.draggingEdge!.target);
        if (index !== -1) {
          this.links.splice(index, 1);
        }
        this.links.push(newEdge);
        const jsonData = this.jsonHandlerService.getJsonData() || {};
        if (jsonData.journal && jsonData.journal.modules) {
          const sourceModule = jsonData.journal.modules[this.draggingEdge.source];
          if (sourceModule) {
            sourceModule.next_id = node.id;
            this.jsonHandlerService.saveJsonData(jsonData);
          }
        }
        this.updateGraph();
      }
      this.isDraggingEdge = false;
    }
  }
}
